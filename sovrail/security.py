import hashlib,hmac,json,time,secrets
from fastapi import HTTPException
from .store import db,now
from .config import settings

def sha(v:str)->str: return hashlib.sha256(v.encode()).hexdigest()

def create_key(name,scopes,rpm,daily_limit,daily_budget_micros,expires_at=None):
    raw='sov_'+secrets.token_urlsafe(32); c=db()
    c.execute('INSERT INTO client_keys(name,key_hash,prefix,scopes,rpm,daily_limit,daily_budget_micros,expires_at,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(name,sha(raw),raw[:12],','.join(sorted(set(scopes))),rpm,daily_limit,daily_budget_micros,expires_at,now()))
    c.commit(); audit('key.created',{'name':name,'prefix':raw[:12],'scopes':scopes}); return raw

def verify_key(raw,required_scope=None):
    if not raw or not raw.startswith('sov_'): raise HTTPException(401,'Missing or invalid SOVRAIL key')
    c=db(); row=c.execute('SELECT * FROM client_keys WHERE key_hash=? AND enabled=1',(sha(raw),)).fetchone()
    if not row: raise HTTPException(401,'Unknown or disabled SOVRAIL key')
    if row['expires_at'] and row['expires_at'] < now(): raise HTTPException(401,'Expired SOVRAIL key')
    scopes=set(filter(None,row['scopes'].split(',')))
    if required_scope and '*' not in scopes and required_scope not in scopes: raise HTTPException(403,f'Missing scope: {required_scope}')
    return row

def verify_signature(raw_key,method,path,body,ts,signature):
    if not settings.require_signatures: return
    if not ts or not signature: raise HTTPException(401,'Signed request required')
    try: t=int(ts)
    except: raise HTTPException(401,'Invalid signature timestamp')
    if abs(now()-t)>settings.signature_skew_seconds: raise HTTPException(401,'Stale signed request')
    msg=f'{t}\n{method.upper()}\n{path}\n{hashlib.sha256(body).hexdigest()}'.encode()
    expected=hmac.new(raw_key.encode(),msg,hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected,signature): raise HTTPException(401,'Invalid request signature')

def audit(event,payload):
    c=db(); prev=c.execute('SELECT event_hash FROM audit ORDER BY id DESC LIMIT 1').fetchone(); ph=prev['event_hash'] if prev else 'GENESIS'
    data=json.dumps(payload,sort_keys=True,separators=(',',':')); eh=sha(ph+'|'+event+'|'+data)
    c.execute('INSERT INTO audit(event,payload,prev_hash,event_hash,created_at) VALUES(?,?,?,?,?)',(event,data,ph,eh,now())); c.commit()
