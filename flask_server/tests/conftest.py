import pytest

from run import app

@pytest.fixture
def client(request):
    client = app.test_client()
    return client
