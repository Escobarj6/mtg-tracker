from mtg_api.db import get_engine
from mtg_api.main import app
from sqlalchemy import create_engine


def test_health_ok_when_database_reachable(client):
    engine = create_engine("sqlite://")
    app.dependency_overrides[get_engine] = lambda: engine

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "available"}


def test_health_503_when_database_unreachable(client, tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'missing' / 'mtg.db'}")
    app.dependency_overrides[get_engine] = lambda: engine

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"detail": "database unavailable"}
