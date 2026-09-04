import hashlib,hmac,json,time,httpx

class SovrailClient:
    def __init__(self,base_url,key,timeout=180,sign_requests=False):
        self.base_url=base_url.rstrip('/'); self.key=key; self.timeout=timeout; self.sign_requests=sign_requests
    def _headers(self,method,path,body=b'',idempotency_key=None):
        h={'x-sovrail-key':self.key,'content-type':'application/json'}
        if idempotency_key:h['idempotency-key']=idempotency_key
        if self.sign_requests:
            ts=str(int(time.time())); msg=f'{ts}\n{method}\n{path}\n{hashlib.sha256(body).hexdigest()}'.encode(); h['x-sovrail-timestamp']=ts; h['x-sovrail-signature']=hmac.new(self.key.encode(),msg,hashlib.sha256).hexdigest()
        return h
    def chat(self,messages,provider='auto',model=None,max_tokens=1024,cache_ttl=0,route=None,idempotency_key=None):
        path='/v1/chat/completions'; payload={'messages':messages,'provider':provider,'model':model,'max_tokens':max_tokens,'cache_ttl':cache_ttl,'route':route}; body=json.dumps(payload,separators=(',',':')).encode()
        with httpx.Client(timeout=self.timeout) as c:
            r=c.post(self.base_url+path,content=body,headers=self._headers('POST',path,body,idempotency_key)); r.raise_for_status(); return r.json()
