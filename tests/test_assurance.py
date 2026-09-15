import os
os.environ.setdefault('SOVRAIL_MASTER_KEY','test-master')
from fastapi.testclient import TestClient
from sovrail.secure_main import app

client=TestClient(app)
HEAD={'Authorization':'Bearer test-master'}

def test_unauthorized_external_effect_blocks_and_contains():
    r=client.post('/v1/assurance/effect',headers=HEAD,json={'agent_id':'a1','action_id':'x1','system':'crm','resource':'customer/1','before_state':{'tier':'basic'},'after_state':{'tier':'admin'},'authorized_effect':False,'external_write':True,'evidence':{}})
    assert r.status_code==200
    assert r.json()['decision']=='block_and_contain'

def test_stale_context_requires_review():
    r=client.post('/v1/assurance/context',headers=HEAD,json={'agent_id':'a1','sources':[{'name':'inventory','stale':True}]})
    assert r.status_code==200
    assert r.json()['decision']=='review'

def test_high_risk_cache_is_forbidden():
    r=client.post('/v1/assurance/cache-decision',headers=HEAD,json={'risk':'critical','tenant':'t1','authorization_scope_hash':'h','freshness_seconds':0,'ttl_seconds':60,'similarity':1.0})
    assert r.status_code==200
    assert r.json()['payload']['decision']=='CACHE_FORBIDDEN'
