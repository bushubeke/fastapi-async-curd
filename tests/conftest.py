import pytest
from fastapi.testclient import TestClient
from app.main import create_dev_app


app=create_dev_app()

@pytest.fixture(scope="module")
def testing_client():
    yield  TestClient(app)
