from sovrail.execution_governor import ExecutionGovernor,GovernorPolicy,ProgressReceipt


def test_governor_budget_and_progress_decisions():
    g=ExecutionGovernor(GovernorPolicy(total_budget=100,protected_reserve=10))
    s=g.new_job('finish coding job')
    g.record_cost(s,60)
    assert g.mode(s)=='conserve'
    g.record_progress(s,ProgressReceipt(changed_files=3,tests_passed=2))
    assert g.decision(s)['model_tier']=='luna-light'
    g.record_cost(s,30)
    assert g.decision(s)['action']=='stop'
