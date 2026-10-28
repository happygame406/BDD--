import uuid
import requests
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("petstore.feature")

def uid():
    return uuid.uuid4().hex[:8]

BODIES = {
    "pet body": lambda ctx: {"name": f"p_{uid()}", "photoUrls": [], "status": "available"},
    "pet body and id": lambda ctx: {"id": ctx["pet_id"], "name": f"p_{uid()}", "photoUrls": [], "status": "available"},
    "order body": lambda ctx: {"id": 0, "petId": 1, "quantity": 1, "status": "placed", "complete": False},
    "user body": lambda ctx: {"id": 0, "username": f"u_{uid()}", "password": "pass123", "userStatus": 1},
}

@given("the API base URL", target_fixture="url")
def url(base_url):
    return base_url

@given("a pet exists", target_fixture="ctx")
def pet_exists(url, ctx):
    r = requests.post(f"{url}/pet", json=BODIES["pet body"](ctx), timeout=10)
    assert r.status_code == 200
    ctx["pet_id"] = r.json()["id"]
    return ctx

@given("an order exists", target_fixture="ctx")
def order_exists(url, ctx):
    r = requests.post(f"{url}/store/order", json=BODIES["order body"](ctx), timeout=10)
    assert r.status_code == 200
    ctx["order_id"] = r.json()["id"]
    return ctx

@given("a user exists", target_fixture="ctx")
def user_exists(url, ctx):
    body = BODIES["user body"](ctx)
    requests.post(f"{url}/user", json=body, timeout=10)
    ctx["username"] = body["username"]
    return ctx

@when(parsers.parse('I POST "{path}" with {kind}'), target_fixture="ctx")
def post(url, ctx, path, kind):
    ctx["resp"] = requests.post(f"{url}{path}", json=BODIES[kind](ctx), timeout=10)
    return ctx

@when(parsers.parse('I PUT "{path}" with {kind}'), target_fixture="ctx")
def put(url, ctx, path, kind):
    ctx["resp"] = requests.put(f"{url}{path}", json=BODIES[kind](ctx), timeout=10)
    return ctx

@when(parsers.parse('I GET "{path}"'), target_fixture="ctx")
def get(url, ctx, path):
    ctx["resp"] = requests.get(f"{url}{path.format(**ctx)}", timeout=10)
    return ctx

@when('I GET "/user/login" with user credentials', target_fixture="ctx")
def login(url, ctx):
    ctx["resp"] = requests.get(
        f"{url}/user/login",
        params={"username": ctx["username"], "password": "pass123"},
        timeout=10,
    )
    return ctx

@then(parsers.parse("status is {code:d}"))
def check_status(ctx, code):
    assert ctx["resp"].status_code == code, ctx["resp"].text

@then(parsers.parse('body has "{key}"'))
def check_key(ctx, key):
    assert key in ctx["resp"].json()