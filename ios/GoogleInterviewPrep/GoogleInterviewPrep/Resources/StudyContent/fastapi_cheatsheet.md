# FastAPI cheat sheet

**Baseline:** FastAPI **0.141.1** · Pydantic **v2** · Starlette · Uvicorn · Python **3.10+** (examples can use 3.12+).

Sections are reference fragments, not one concatenated application: repeated `app = FastAPI()` and repeated routes represent alternatives. Reuse imports as needed. Application-specific persistence/configuration must be supplied where indicated.

Install: `uv add "fastapi[standard]==0.141.1"` or `pip install "fastapi[standard]==0.141.1"`; lock transitive dependencies too.  
Run: `fastapi dev` (reload) · `fastapi run` (prod) · `uvicorn app.main:app --workers 4`

Stack: **Starlette** (ASGI) + **Pydantic v2** (validation) + OpenAPI (`/docs`, `/redoc`, `/openapi.json`).

---

## 1. Minimal app

```python
from fastapi import FastAPI

app = FastAPI(title="Orders", version="1.0.0")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

`def` vs `async def`: use `async def` if you `await`. A sync `def` is run in a threadpool so it does not block the event loop. Don’t call blocking I/O inside `async def` (use `asyncio.to_thread` or a sync `def`).

That offloading applies to FastAPI-invoked sync endpoints and dependencies. Calling an ordinary sync helper yourself from an async endpoint runs it on the event-loop thread unless you explicitly offload it.

---

## 2. Path / query / body (Annotated is the current style)

```python
from typing import Annotated
from fastapi import FastAPI, Path, Query, Body, Header, Cookie
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    price: float = Field(gt=0)
    tags: list[str] = Field(default_factory=list)

@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[int, Path(ge=1)],
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return {"item_id": item_id, "q": q, "limit": limit}

@app.post("/items/", status_code=201)
async def create_item(item: Item):          # JSON body — inferred
    return item

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    note: Annotated[str | None, Body()] = None,  # extra body field
):
    return {"id": item_id, "item": item, "note": note}
```

**Parameter source (FastAPI infers):**
- Simple types (`int`, `str`, `bool`) that are **not** in the path → **query**
- Pydantic model → **JSON body**
- `Path` / `Query` / `Header` / `Cookie` / `Body` / `Form` / `File` to force

The price example demonstrates validation. For monetary amounts, use constrained `Decimal` or integer minor units and define the JSON representation explicitly.

---

## 3. Pydantic v2 models (this is not v1)

```python
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator

class UserIn(BaseModel):
    model_config = ConfigDict(extra="forbid")  # never silently strip a password
    email: EmailStr
    password: str = Field(min_length=8)
    age: int | None = None

    @field_validator("password")
    @classmethod
    def strong(cls, v: str) -> str:
        if v.isdigit():
            raise ValueError("password too weak")
        return v

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # ORM objects
    id: int
    email: EmailStr

class UserInDB(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str  # no plaintext password in persisted models
```

v1 → v2: `orm_mode` → `from_attributes`; `class Config` → `model_config`; `.dict()` → `.model_dump()`; `.json()` → `.model_dump_json()`; `regex=` → `pattern=`.

**Input vs output:** never return `UserIn` with password. `response_model=UserOut` filters fields.

```python
@app.post("/users/", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    return UserOut(id=1, email=user.email)
```

Return-type annotation is also a response model:

```python
@app.get("/users/{uid}", response_model=UserOut)
async def get_user(uid: int) -> UserOut:
    return UserOut(id=uid, email="a@x.com")
```

---

## 4. Query / Header / Cookie / Form **models** (0.115+)

```python
from fastapi import Query, Header, Cookie, Form

class Page(BaseModel):
    model_config = ConfigDict(extra="forbid")  # reject unknown query keys
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
    q: str | None = None

@app.get("/search")
async def search(page: Annotated[Page, Query()]):
    return page

class AuthHeaders(BaseModel):
    x_token: str
    user_agent: str | None = None

@app.get("/me")
async def me(h: Annotated[AuthHeaders, Header(convert_underscores=True)]):
    return {"user_agent": h.user_agent}  # do not echo authentication secrets

class LoginForm(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(form: Annotated[LoginForm, Form()]):
    return {"user": form.username}
```

---

## 5. Files, forms, uploads

```python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload(
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()] = "",
):
    from fastapi import HTTPException
    size = 0
    try:
        while chunk := await file.read(64 * 1024):
            size += len(chunk)
            if size > 10 * 1024 * 1024:
                raise HTTPException(413, "file too large")
            # stream chunk to storage here
        return {"name": file.filename, "n": size, "desc": description}
    finally:
        await file.close()
```

`bytes` + `File()` and unbounded `await file.read()` load the whole file into memory. `UploadFile` spools to disk after its memory threshold; chunk reads bound application memory. Also enforce request-size limits at the proxy/parser: this handler runs after multipart parsing.

---

## 6. Status codes, errors, extra responses

```python
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

@app.get("/items/{item_id}")
async def get(item_id: int):
    if item_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="item not found",
            headers={"X-Error": "not-found"},
        )
    return {"id": item_id}

from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exc_handler(request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"error": exc.detail}, headers=exc.headers
    )  # preserve WWW-Authenticate, Retry-After, etc.
```

Missing credentials in the built-in security classes changed from 403 to **401 in 0.122.0**. Use 401 + an appropriate `WWW-Authenticate` challenge for invalid/missing bearer credentials; 403 for an authenticated caller lacking permission. Request validation normally produces 422; response-model validation failure indicates a server bug.

---

## 7. Dependencies (the real framework)

```python
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="token")

# Async SQLAlchemy session factory from section 13.
async def get_db():
    async with SessionLocal() as db:
        yield db

async def get_current_user(token: Annotated[str, Depends(oauth2)]):
    claims = decode_token(token)  # signature/expiry/issuer/audience checked in section 8
    user = lookup_user(claims["sub"])
    if not user or user["disabled"]:
        raise HTTPException(401, "bad token", headers={"WWW-Authenticate": "Bearer"})
    return {"id": user["id"], "username": user["username"]}

@app.get("/me")
async def me(user: Annotated[dict, Depends(get_current_user)]):
    return user
```

- Sub-dependencies compose. Classes with `__call__` work as deps.
- `yield` deps: default `scope="request"` cleans up after the response; `scope="function"` cleans up before sending it. Always re-raise exceptions you catch unless deliberately replacing them. Background jobs should open their own resources and accept IDs, not request-scoped sessions.
- Override in tests: `app.dependency_overrides[get_db] = lambda: fake_db`
- Router-level: `APIRouter(dependencies=[Depends(require_auth)])`
- App-level: `FastAPI(dependencies=[Depends(log_request)])`

```python
from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["orders"], dependencies=[Depends(get_current_user)])

@router.get("/orders")
async def list_orders():
    return []

app.include_router(router)
```

---

## 8. Security: password verification + JWT (local demo)

Install `pyjwt` and `pwdlib[argon2]`. Set `JWT_SECRET` to a randomly generated secret with at least 32 bytes of entropy (for example, generate it with `openssl rand -hex 32`). The in-memory account below is a demo fixture; replace it with a user store. For delegated browser login, use an identity provider with authorization code + PKCE.

```python
from datetime import datetime, timedelta, timezone
import os
import jwt  # PyJWT, not python-jose
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm

pwd = PasswordHash.recommended()
SECRET, ALG = os.environ["JWT_SECRET"], "HS256"
ISSUER, AUDIENCE = "orders-auth", "orders-api"
USERS = {
    "alice": {"id": 1, "username": "alice", "disabled": False,
              "hashed_password": pwd.hash("demo-password")}
}
DUMMY_HASH = pwd.hash("dummy-password")

def lookup_user(username: str):
    return USERS.get(username)

def create_token(sub: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode(
        {"sub": sub, "exp": exp, "iss": ISSUER, "aud": AUDIENCE}, SECRET, algorithm=ALG
    )

def decode_token(token: str) -> dict:
    try:
        claims = jwt.decode(
            token, SECRET, algorithms=[ALG], issuer=ISSUER, audience=AUDIENCE,
            options={"require": ["exp", "sub", "iss", "aud"]},
        )
        if not isinstance(claims["sub"], str) or not claims["sub"]:
            raise InvalidTokenError("missing subject")
        return claims
    except InvalidTokenError as exc:
        raise HTTPException(401, "bad token", headers={"WWW-Authenticate": "Bearer"}) from exc

@app.post("/token")
def token(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = lookup_user(form.username)
    valid = pwd.verify(form.password, user["hashed_password"] if user else DUMMY_HASH)
    if not user or not valid or user["disabled"]:
        raise HTTPException(401, "bad credentials", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_token(form.username), "token_type": "bearer"}
```

The sync token endpoint offloads password hashing from the event loop. Scopes: `Security(get_current_user, scopes=["orders:write"])` only declares requirements; extend that dependency to accept `SecurityScopes` and verify scopes from validated claims. `OAuth2PasswordBearer` alone extracts a token; it neither validates JWTs nor enforces scopes. HTTP Basic: `HTTPBasic`. API keys: `APIKeyHeader(name="X-API-Key")`.

---

## 9. Middleware, CORS, trusted host

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.example.com", "*.example.com"])
```

Custom:

```python
@app.middleware("http")
async def add_request_id(request, call_next):
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.headers.get("X-Request-ID", "n/a")
    return response
```

Behind a proxy: use Uvicorn `--proxy-headers --forwarded-allow-ips=127.0.0.1` (replace with your proxy addresses). Trust `*` only when network access is restricted to trusted proxies. Set `root_path="/api"` when the proxy strips that prefix; it describes the external mount, not an extra router prefix.

---

## 10. Lifespan (do not use `@app.on_event`)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis  # pip install redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: pool, redis, ml model
    app.state.redis = Redis.from_url("redis://localhost")
    try:
        yield
    finally:
        await app.state.redis.aclose()

app = FastAPI(lifespan=lifespan)
```

---

## 11. Background tasks, SSE, streaming

```python
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse

def write_log(msg: str):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(msg)

@app.post("/notify")
async def notify(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "sent\n")
    return {"queued": True}

@app.get("/stream")
async def stream():
    async def gen():
        yield b"data: hello\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
```

`BackgroundTasks` run **after** the response, in-process — not a job queue. Use Celery / RQ / arq / SAQ for real work.

JSON Lines and SSE have first-class tutorial pages in current docs (`/tutorial/stream-json-lines/`, `/tutorial/server-sent-events/`).

---

## 12. Bigger apps

```
app/
  main.py          # FastAPI(), include_router, middleware
  deps.py          # get_db, get_user
  core/config.py   # pydantic-settings
  routers/items.py
  models/
  schemas/
  services/
```

```python
# core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str
    secret_key: str
    debug: bool = False

settings = Settings()
```

---

## 13. SQLAlchemy 2.x (async example)

Install `sqlalchemy[asyncio]` (includes the required `greenlet` dependency) plus the driver matching the URL, e.g. `asyncpg` for `postgresql+asyncpg://...` or `aiosqlite` for `sqlite+aiosqlite://...`. Create the schema with migrations. Dispose the engine with `await engine.dispose()` during lifespan shutdown.

```python
from sqlalchemy import String, select
from collections.abc import AsyncIterator
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

class Base(DeclarativeBase):
    pass

class ItemRow(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))

engine = create_async_engine(settings.database_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as s:
        yield s

class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

@app.get("/items", response_model=list[ItemOut])
async def list_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    stmt = select(ItemRow).order_by(ItemRow.id).offset(offset).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    return rows  # from_attributes
```

Commit writes inside the endpoint/service transaction (e.g. `async with db.begin():`), before returning success; do not defer a possibly failing commit until after the response. A session is not safe to share between concurrent tasks. For sync SQLAlchemy, use a sync dependency with `with SessionLocal() as db: yield db` and sync `def` routes.

**SQLModel** combines SQLAlchemy and Pydantic. Choose separate input/output schemas to control fields and validation; architecture choices are not tied to an interview level.

---

## 14. Responses other than JSON

```python
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, ORJSONResponse, PlainTextResponse

app = FastAPI(default_response_class=ORJSONResponse)  # pip install orjson

@app.get("/home", response_class=HTMLResponse)
async def home():
    return "<h1>hi</h1>"
```

---

## 15. WebSockets

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text()
            await websocket.send_text(f"echo {msg}")
    except WebSocketDisconnect:
        pass
```

---

## 16. Testing

```python
from fastapi.testclient import TestClient

def test_health():
    with TestClient(app) as client:  # starts/stops lifespan
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["ok"] is True

def test_auth_override():
    app.dependency_overrides[get_current_user] = lambda: {"id": 1}
    try:
        with TestClient(app) as client:
            r = client.get("/me")
            assert r.status_code == 200
    finally:
        app.dependency_overrides.pop(get_current_user, None)
```

Async tests: `httpx.AsyncClient` + `ASGITransport(app=app)` + `pytest-asyncio`. HTTPX's ASGI transport does not start lifespan; use a lifespan manager (e.g. `asgi-lifespan`) or explicitly managed fixtures when resources need startup/shutdown.

---

## 17. Deployment

```bash
fastapi run app/main.py --host 0.0.0.0 --port 8080
# Import-string alternative: fastapi run --entrypoint app.main:app
# or
uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4 --proxy-headers
```

Workers are processes; each owns its own pools and memory. Choose their count by load testing and deployment limits, not a fixed cores multiplier. A single async worker can overlap many I/O waits. Offload expensive CPU work to a process pool or external workers; threads do not automatically parallelize pure Python CPU work on a GIL-enabled build.

Docker: build a small application image and run the FastAPI CLI or Uvicorn. In an orchestrator, consider one worker per container with replica scaling. The old `uvicorn.workers` Gunicorn module is deprecated; use the separate `uvicorn-worker` package when choosing Gunicorn.

Env: `FASTAPI_ENV` documented for CLI. Settings from env via pydantic-settings, never commit secrets.

---

## 18. Performance / Google-interview talking points

- Profile first: DB queries, external I/O, validation and serialization can each dominate. Typed response models use Pydantic's optimized serialization; `ORJSONResponse` is an optional measured choice, not a universal speedup.
- Connection pool size vs worker count (classic: workers × pool > DB `max_connections`)
- Don’t hold a DB session across `await` of slow HTTP calls
- `Depends(yield)` session per request
- Rate limit at gateway (Cloud Armor / Envoy / nginx), not only in Python
- Idempotency keys on POSTs
- OpenAPI is a contract — `response_model` is part of the public API

---

## 19. Common footguns

| Footgun | Fix |
|---|---|
| Blocking `requests.get` in `async def` | `httpx.AsyncClient` or sync `def` |
| Returning ORM object with lazy attrs | `from_attributes` + eager load; or schema |
| Mutable defaults | Ordinary Python defaults share state; Pydantic deep-copies non-hashable defaults, but `Field(default_factory=list)` states intent clearly |
| Pydantic v1 `class Config` on 0.100+ | `model_config = ConfigDict(...)` |
| `@app.on_event("startup")` | `lifespan` |
| `BackgroundTasks` as a queue | Celery/arq |
| CORS `allow_origins=["*"]` + credentials | Forbidden by spec; list origins |
| Putting secrets in query strings | Header / body |
| Sync SQLAlchemy engine with `async def` + no thread | Use `AsyncSession` or `def` |

---

## 20. Version notes (0.100 → 0.141)

- **0.100:** introduced Pydantic v2 support alongside v1
- **0.106 / 0.118:** yield cleanup moved before the response, then back after it (important for streaming)
- **0.111:** `fastapi` CLI (`fastapi dev` / `run`)
- **0.115:** Query/Header/Cookie **models**; `extra="forbid"` on query
- **0.113:** form models; **0.114:** forbid extra form fields
- **0.121:** yield dependency scope control; **0.122:** missing-credential 401 change
- **0.14x:** built-in SSE/JSON Lines documentation, `app.frontend()`, CLI environment options; consult release notes for exact APIs
- **0.141.1:** the baseline used by this sheet, not a perpetual latest-version claim

Use Pydantic v2 for these examples; do not assume v1 models remain supported by this FastAPI baseline. Consult the migration guide when upgrading an older app.

---

## Review notes and official references

All 20 Python fragments passed syntax checks on Python 3.12. Targeted tests used FastAPI 0.141.1/Pydantic 2.13 and covered request/response validation, valid and invalid credentials/JWTs, preserved HTTP headers, upload limits, Redis lifespan entry/exit and SQLAlchemy async pagination against SQLite. No external Redis/PostgreSQL server or production deployment was tested.

- Version changes: [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/).
- Cleanup timing: [yield dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).
- Password and token APIs: [JWT authentication tutorial](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
- Session concurrency and async installation: [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).
- Entry points and command syntax: [FastAPI CLI](https://fastapi.tiangolo.com/fastapi-cli/).
