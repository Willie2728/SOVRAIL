from sovrail.execution_governor import ModelTier
from sovrail.governor_store import create_job,load_job,save_job


def test_job_round_trip():
    key_hash='test-governor-key'
    s=create_job(key_hash,'persistent objective',100,ModelTier.LUNA_LIGHT)
    s.spent=12.5
    s.no_progress_count=1
    save_job(s)
    loaded=load_job(s.job_id,key_hash)
    assert loaded is not None
    assert loaded.objective=='persistent objective'
    assert loaded.spent==12.5
    assert loaded.no_progress_count==1
    assert loaded.tier==ModelTier.LUNA_LIGHT
