import json,time,hashlib
from fastapi import HTTPException
from .store import db,now

def enforce_rate(row):
    c=db(); kh=row['key_hash']; rpm=max(1,row['rpm']); rate=rpm/60.0; capacity=max(5,rpm)
    r=c.execute('SELECT * FROM rate_bucket WHERE key_hash=?',(kh,)).fetchone(); t=time.time()
    tokens=capacity if not r else min(capacity,r['tokens']+(t-r['updated_at'])*rate)
    if tokens<1: raise HTTPException(429,'Rate limit exceeded')
    c.execute('INSERT OR REPLACE INTO rate_bucket(key_hash,tokens,updated_at) VALUES(?,?,?)',(kh,tokens-1,t)); c.commit()

def enforce_daily(row):
    c=db(); since=now()-86400
    u=c.execute('SELECT COUNT(*) n,COALESCE(SUM(cost_micros),0) cost FROM usage WHERE key_hash=? AND created_at>=?',(row['key_hash'],since)).fetchone()
    if u['n']>=row['daily_limit']: raise HTTPException(429,'Daily request limit reached')
    if row['daily_budget_micros'] and u['cost']>=row['daily_budget_micros']: raise HTTPException(402,'Daily upstream budget reached')

def cache_key(namespace,obj): return hashlib.sha256((namespace+'|'+json.dumps(obj,sort_keys=True,separators=(',',':'))).encode()).hexdigest()
def cache_get(k):
    c=db(); r=c.execute('SELECT payload FROM cache WHERE cache_key=? AND expires_at>?',(k,now())).fetchone(); return json.loads(r['payload']) if r else None
def cache_put(k,payload,ttl):
    if ttl<=0:return
    c=db(); c.execute('INSERT OR REPLACE INTO cache VALUES(?,?,?)',(k,json.dumps(payload),now()+ttl)); c.commit()

def idem_get(kh,key):
    if not key:return None
    c=db(); r=c.execute('SELECT response FROM idempotency WHERE key_hash=? AND idem_key=? AND expires_at>?',(kh,key,now())).fetchone(); return json.loads(r['response']) if r else None
def idem_put(kh,key,response,ttl=86400):
    if not key:return
    c=db(); c.execute('INSERT OR REPLACE INTO idempotency VALUES(?,?,?,?)',(kh,key,json.dumps(response),now()+ttl)); c.commit()

def circuit_allowed(provider):
    c=db(); r=c.execute('SELECT * FROM circuits WHERE provider=?',(provider,)).fetchone(); return not r or r['opened_until']<=now()
def circuit_success(provider):
    c=db(); c.execute('INSERT OR REPLACE INTO circuits(provider,failures,opened_until) VALUES(?,?,?)',(provider,0,0)); c.commit()
def circuit_failure(provider,threshold=3,cooldown=60):
    c=db(); r=c.execute('SELECT * FROM circuits WHERE provider=?',(provider,)).fetchone(); f=(r['failures'] if r else 0)+1; opened=now()+cooldown if f>=threshold else 0
    c.execute('INSERT OR REPLACE INTO circuits(provider,failures,opened_until) VALUES(?,?,?)',(provider,f,opened)); c.commit()
