import pytest

def pytest_addoption(parser):
    parser.addoption("--base-url", default="https://petstore.swagger.io/v2")

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")

@pytest.fixture
def ctx():
    return {}