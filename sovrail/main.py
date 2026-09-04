import time
from typing import Any,Optional
import httpx
from fastapi import FastAPI,HTTPException,Header,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from .config import settings
from .store import db,now
from .security import create_key,verify_key,verify_signature,audit
from .controls import enforce_rate,enforce_daily,cache_key,cache_get,cache_put,idem_get,idem_put,circuit_allowed,circuit_success,circuit_failure
from .providers import local_chat,openai_chat,anthropic_chat

app=FastAPI(title='SOVRAIL AI — API Gateway Intelligence',version='2.1.0')

class KeyCreate(BaseModel):
    name:str; scopes:list[str]=['chat']; rpm:int=Field(120,ge=1,le=100000); daily_limit:int=Field(5000,ge=1); daily_budget_micros:int=Field(0,ge=0); expires_at:Optional[int]=None
class ChatReq(BaseModel):
    messages:list[dict[str,Any]]; model:Optional[str]=None; provider:str='auto'; max_tokens:int=Field(1024,ge=1,le=65536); cache_ttl:int=Field(0,ge=0,le=604800); route:list[str]|None=None

@app.on_event('startup')
def startup(): db().close()

@app.get('/health')
def health():
    return {'ok':True,'version':'2.1.0','providers':{'local':True,'openai':bool(settings.openai_key and settings.openai_model),'anthropic':bool(settings.anthropic_key and settings.anthropic_model),'tavus':bool(settings.tavus_key)},'signed_requests':settings.require_signatures}

@app.post('/admin/keys')
def admin_create(body:KeyCreate,authorization:Optional[str]=Header(None)):
    if not settings.master_key or authorization!=f'Bearer {settings.master_key}': raise HTTPException(401,'Master authorization required')
    raw=create_key(body.name,body.scopes,body.rpm,body.daily_limit,body.daily_budget_micros,body.expires_at)
    return {'name':body.name,'api_key':raw,'scopes':body.scopes,'warning':'Shown once; store securely'}

@app.post('/admin/keys/{prefix}/revoke')
def admin_revoke(prefix:str,authorization:Optional[str]=Header(None)):
    if not settings.master_key or authorization!=f'Bearer {settings.master_key}': raise HTTPException(401,'Master authorization required')
    c=db(); cur=c.execute('UPDATE client_keys SET enabled=0 WHERE prefix=?',(prefix,)); c.commit(); audit('key.revoked',{'prefix':prefix}); return {'revoked':cur.rowcount}

async def auth_request(request:Request,key:str|None,scope:str):
    raw=await request.body(); row=verify_key(key,scope); verify_signature(key or '',request.method,request.url.path,raw,request.headers.get('x-sovrail-timestamp'),request.headers.get('x-sovrail-signature')); enforce_rate(row); enforce_daily(row); return row

def log(kh,provider,endpoint,status,cost=0,lat=0):
    c=db(); c.execute('INSERT INTO usage(key_hash,provider,endpoint,status,cost_micros,latency_ms,created_at) VALUES(?,?,?,?,?,?,?)',(kh,provider,endpoint,status,cost,lat,now())); c.commit()

@app.post('/v1/chat/completions')
async def chat(request:Request,body:ChatReq,x_sovrail_key:Optional[str]=Header(None),idempotency_key:Optional[str]=Header(None)):
    row=await auth_request(request,x_sovrail_key,'chat'); kh=row['key_hash']; old=idem_get(kh,idempotency_key)
    if old is not None:return {'idempotent_replay':True,**old}
    ck=cache_key(settings.cache_namespace,body.model_dump()); hit=cache_get(ck)
    if hit is not None: log(kh,'cache','/v1/chat/completions',200); return {'cached':True,**hit}
    order=body.route or ([body.provider] if body.provider!='auto' else ['local','openai','anthropic'])
    errors=[]; t=time.time()
    for p in order:
        if p not in {'local','openai','anthropic'}: continue
        if not circuit_allowed(p): errors.append(f'{p}: circuit open'); continue
        try:
            out=await {'local':local_chat,'openai':openai_chat,'anthropic':anthropic_chat}[p](body.messages,body.model,body.max_tokens)
            circuit_success(p); lat=int((time.time()-t)*1000); log(kh,p,'/v1/chat/completions',200,0,lat); cache_put(ck,out,body.cache_ttl); idem_put(kh,idempotency_key,out); return out
        except Exception as e:
            circuit_failure(p); errors.append(f'{p}: {str(e)[:300]}')
            if body.provider!='auto' and not body.route: break
    log(kh,body.provider,'/v1/chat/completions',502,0,int((time.time()-t)*1000)); raise HTTPException(502,{'message':'All routes failed','errors':errors})

@app.api_route('/v1/tavus/{path:path}',methods=['GET','POST','PUT','PATCH','DELETE'])
async def tavus(path:str,request:Request,x_sovrail_key:Optional[str]=Header(None)):
    row=await auth_request(request,x_sovrail_key,'tavus'); kh=row['key_hash']
    if not settings.tavus_key: raise HTTPException(503,'Tavus not configured')
    if '..' in path or path.startswith('/') or '://' in path: raise HTTPException(400,'Invalid upstream path')
    raw=await request.body(); headers={'x-api-key':settings.tavus_key}
    if request.headers.get('content-type'): headers['content-type']=request.headers['content-type']
    t=time.time()
    async with httpx.AsyncClient(timeout=settings.request_timeout,follow_redirects=False) as c:
        r=await c.request(request.method,f'{settings.allowed_tavus_host.rstrip("/")}/{path}',content=raw,headers=headers,params=request.query_params)
    log(kh,'tavus',f'/v1/tavus/{path}',r.status_code,0,int((time.time()-t)*1000))
    ctype=r.headers.get('content-type',''); return JSONResponse(status_code=r.status_code,content=r.json() if 'application/json' in ctype else {'body':r.text})

@app.get('/v1/usage')
def usage(x_sovrail_key:Optional[str]=Header(None)):
    row=verify_key(x_sovrail_key,'usage'); c=db(); since=now()-86400
    r=c.execute('SELECT COUNT(*) requests,COALESCE(SUM(cost_micros),0) cost_micros,COALESCE(AVG(latency_ms),0) avg_latency_ms FROM usage WHERE key_hash=? AND created_at>=?',(row['key_hash'],since)).fetchone(); return dict(r)
