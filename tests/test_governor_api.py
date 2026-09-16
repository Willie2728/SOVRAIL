from fastapi.testclient import TestClient
from sovrail.main import app


def test_health_advertises_governor():
    c=TestClient(app)
    r=c.get('/health')
    assert r.status_code == 200
    assert r.json()['execution_governor'] is True
    assert r.json()['version'] == '2.4.0'


def test_governor_routes_exist():
    paths={r.path for r in app.routes}
    assert '/v1/governor/jobs' in paths
    assert '/v1/governor/jobs/{job_id}/events' in paths
    assert '/v1/governor/jobs/{job_id}' in paths
