import pytest
from fastapi.testclient import TestClient
from mtg_api.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
