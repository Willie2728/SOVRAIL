import httpx
from fastapi import HTTPException
from .config import settings

async def local_chat(messages,model=None,max_tokens=1024):
    m=model or settings.local_model
    async with httpx.AsyncClient(timeout=settings.request_timeout) as c:
        r=await c.post(f'{settings.ollama_url}/api/chat',json={'model':m,'messages':messages,'stream':False,'options':{'num_predict':max_tokens}}); r.raise_for_status(); d=r.json()
    return {'provider':'local','model':m,'choices':[{'message':d.get('message',{})}],'usage':{'output_tokens':d.get('eval_count')}}

async def openai_chat(messages,model=None,max_tokens=1024):
    if not settings.openai_key or not (model or settings.openai_model): raise HTTPException(503,'OpenAI not configured')
    m=model or settings.openai_model
    async with httpx.AsyncClient(timeout=settings.request_timeout) as c:
        r=await c.post('https://api.openai.com/v1/responses',headers={'Authorization':f'Bearer {settings.openai_key}'},json={'model':m,'input':messages,'max_output_tokens':max_tokens})
        if r.status_code>=400: raise HTTPException(r.status_code,r.text)
        d=r.json()
    text=''.join(x.get('text','') for item in d.get('output',[]) for x in item.get('content',[]) if x.get('type') in ('output_text','text'))
    return {'provider':'openai','model':m,'choices':[{'message':{'role':'assistant','content':text}}],'usage':d.get('usage'),'upstream_id':d.get('id')}

async def anthropic_chat(messages,model=None,max_tokens=1024):
    if not settings.anthropic_key or not (model or settings.anthropic_model): raise HTTPException(503,'Anthropic not configured')
    m=model or settings.anthropic_model; system=[]; msgs=[]
    for x in messages:
        (system if x.get('role')=='system' else msgs).append(x.get('content','') if x.get('role')=='system' else {'role':x.get('role','user'),'content':x.get('content','')})
    p={'model':m,'max_tokens':max_tokens,'messages':msgs}
    if system:p['system']='\n'.join(system)
    async with httpx.AsyncClient(timeout=settings.request_timeout) as c:
        r=await c.post('https://api.anthropic.com/v1/messages',headers={'x-api-key':settings.anthropic_key,'anthropic-version':'2023-06-01'},json=p)
        if r.status_code>=400: raise HTTPException(r.status_code,r.text)
        d=r.json()
    text=''.join(x.get('text','') for x in d.get('content',[]) if x.get('type')=='text')
    return {'provider':'anthropic','model':m,'choices':[{'message':{'role':'assistant','content':text}}],'usage':d.get('usage'),'upstream_id':d.get('id')}
