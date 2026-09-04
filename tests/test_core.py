import os,tempfile,importlib

def setup_module():
    os.environ['SOVRAIL_DB_PATH']=tempfile.mktemp(suffix='.db')
    os.environ['SOVRAIL_MASTER_KEY']='test-master'

def test_security_and_limits():
    import sovrail.config as cfg; importlib.reload(cfg)
    import sovrail.store as st; importlib.reload(st)
    import sovrail.security as sec; importlib.reload(sec)
    import sovrail.controls as ctl; importlib.reload(ctl)
    raw=sec.create_key('asset',['chat','usage'],10,100,1000000)
    row=sec.verify_key(raw,'chat'); assert row['name']=='asset'
    ctl.enforce_rate(row); ctl.enforce_daily(row)
    sec.audit('test',{'ok':True}); c=st.db(); a=c.execute('SELECT * FROM audit').fetchall(); assert len(a)>=2

def test_cache_idempotency():
    import sovrail.controls as ctl
    k=ctl.cache_key('x',{'a':1}); ctl.cache_put(k,{'ok':1},30); assert ctl.cache_get(k)=={'ok':1}
    ctl.idem_put('kh','id1',{'x':2},30); assert ctl.idem_get('kh','id1')=={'x':2}
