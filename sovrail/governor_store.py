import json
import uuid
from .store import db, now
from .execution_governor import ExecutionState, ModelTier, ProgressReceipt


def create_job(key_hash: str, objective: str, total_budget: float, tier: ModelTier) -> ExecutionState:
    job_id = uuid.uuid4().hex
    t = now(); c = db()
    c.execute('INSERT INTO execution_jobs(id,key_hash,objective,total_budget,spent,tier,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)',
              (job_id,key_hash,objective,total_budget,0,tier.value,'active',t,t)); c.commit()
    state = ExecutionState(objective=objective, tier=tier)
    setattr(state, 'job_id', job_id)
    return state


def load_job(job_id: str, key_hash: str):
    c=db(); r=c.execute('SELECT * FROM execution_jobs WHERE id=? AND key_hash=?',(job_id,key_hash)).fetchone()
    if not r:return None
    s=ExecutionState(objective=r['objective'],spent=float(r['spent']),tier=ModelTier(r['tier']),
        same_failure_count=r['same_failure_count'],no_progress_count=r['no_progress_count'],
        last_failure=r['last_failure'],last_progress_fingerprint=r['last_progress_fingerprint'])
    setattr(s,'job_id',r['id']); setattr(s,'total_budget',float(r['total_budget'])); return s


def save_job(state: ExecutionState, status: str='active'):
    c=db(); c.execute('UPDATE execution_jobs SET spent=?,tier=?,same_failure_count=?,no_progress_count=?,last_failure=?,last_progress_fingerprint=?,status=?,updated_at=? WHERE id=?',
        (state.spent,state.tier.value,state.same_failure_count,state.no_progress_count,state.last_failure,state.last_progress_fingerprint,status,now(),state.job_id)); c.commit()


def add_event(job_id: str,event_type: str,payload: dict):
    c=db(); c.execute('INSERT INTO execution_events(job_id,event_type,payload,created_at) VALUES(?,?,?,?)',(job_id,event_type,json.dumps(payload,sort_keys=True),now())); c.commit()


def list_events(job_id: str):
    c=db(); rows=c.execute('SELECT event_type,payload,created_at FROM execution_events WHERE job_id=? ORDER BY id',(job_id,)).fetchall()
    return [{'event_type':r['event_type'],'payload':json.loads(r['payload']),'created_at':r['created_at']} for r in rows]
