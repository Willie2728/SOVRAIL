from sovrail.execution_governor import ExecutionGovernor, GovernorPolicy, ModelTier, ProgressReceipt


def test_starts_cheap_and_deescalates_after_progress():
    g = ExecutionGovernor()
    s = g.new_job("build application")
    assert s.tier == ModelTier.LUNA_LIGHT
    g.record_failure(s, "same blocker")
    g.record_failure(s, "same blocker")
    assert g.should_reroute(s)
    assert g.escalate(s) == ModelTier.LUNA_MEDIUM
    g.record_progress(s, ProgressReceipt(changed_files=2, tests_passed=3))
    assert s.tier == ModelTier.LUNA_LIGHT


def test_budget_modes_and_protected_reserve():
    g = ExecutionGovernor(GovernorPolicy(total_budget=100, protected_reserve=10))
    s = g.new_job("job")
    g.record_cost(s, 60)
    assert g.mode(s) == "conserve"
    g.record_cost(s, 15)
    assert g.mode(s) == "essential-only"
    g.record_cost(s, 10)
    assert g.mode(s) == "checkpoint"
    g.record_cost(s, 5)
    assert g.mode(s) == "stop"
    assert not g.may_execute(s)


def test_no_progress_causes_reroute():
    g = ExecutionGovernor()
    s = g.new_job("job")
    g.record_progress(s, ProgressReceipt())
    g.record_progress(s, ProgressReceipt())
    assert g.should_reroute(s)
    assert g.decision(s)["action"] == "escalate"
