# Django cheat sheet

**Baseline:** Django **6.1** APIs · **LTS: 5.2.x** (until Apr 2028) · Python **3.12–3.14**. Use a supported patch release and lock the resolved dependencies; version-specific examples below are not all compatible with 5.2.

Sections are reference fragments for separate project files, not one executable script. Start with generated project settings and merge the settings below. Domain names such as `Item`, `User.credit_limit`, and `queue_job` require your own implementation.

Next LTS: **6.2** (Apr 2027). After that, calendar versions: **2028**, **2029**.

```bash
python -m pip install "Django>=6.1,<6.2" "psycopg[binary]"
django-admin startproject config .
python manage.py startapp orders
python manage.py migrate
python manage.py runserver
```

Production: an appropriate WSGI/ASGI server behind a reverse proxy, **never** `runserver`. ASGI (`config.asgi:application`) supports async HTTP; WebSockets need additional routing/consumers such as Django Channels, not just Django's ASGI handler.

---

## 1. Project layout

```
config/                 # project package (name it, don't leave as mysite)
  settings/
    base.py, dev.py, prod.py
  urls.py
  asgi.py
  wsgi.py
orders/
  models.py
  views.py
  urls.py
  services.py           # keep views thin
  selectors.py
  admin.py
  migrations/
manage.py
```

Split settings: `DJANGO_SETTINGS_MODULE=config.settings.prod`.

---

## 2. Settings that matter

```python
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]  # config/settings/base.py

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ["api.example.com"]

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth",
    "django.contrib.contenttypes", "django.contrib.sessions",
    "django.contrib.messages", "django.contrib.staticfiles",
    "django.contrib.postgres",
    "orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django.middleware.csp.ContentSecurityPolicyMiddleware",  # Django 6.0+
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "app", "USER": "app", "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": "127.0.0.1", "PORT": "5432",
        "CONN_MAX_AGE": 60,          # persistent conns per worker
        "OPTIONS": {"connect_timeout": 5},
    }
}

# Default auth.User is used here. For a custom user, create accounts.User,
# install "accounts", and set AUTH_USER_MODEL BEFORE the first migration.
# AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STORAGES = {                         # 4.2+  (not DEFAULT_FILE_STORAGE)
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Django 6.1 mailers (EMAIL_* deprecated → gone in 2028)
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {"host": "smtp.example.com", "use_tls": True},
    }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # enable only after HTTPS works everywhere required
```

Django 6.1 DB support: **PostgreSQL 15+**, **MySQL 8.4+**, **MariaDB 10.11+**, **SQLite 3.37+**.

---

## 3. Models

```python
from django.conf import settings
from django.db import models

class Order(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        PAID = "paid", "Paid"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DB_CASCADE,   # 6.1: SQL ON DELETE CASCADE (no Django signals)
        related_name="orders",
    )
    status = models.CharField(max_length=8, choices=Status, default=Status.OPEN)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]
        constraints = [
            models.CheckConstraint(condition=models.Q(total__gte=0), name="total_gte_0"),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk}"
```

**`on_delete` (6.1):**

- Django-managed: `CASCADE`, `PROTECT`, `RESTRICT`, `SET_NULL`, `SET_DEFAULT`, `DO_NOTHING`. These do not all delete rows or emit delete signals: `PROTECT`/`RESTRICT` block deletion; `DO_NOTHING` leaves enforcement to the DB. Cascades can use fast deletion when signals and relations allow it.
- DB-managed: `DB_CASCADE`, `DB_SET_NULL`, `DB_SET_DEFAULT`. Rows cascaded by the database do not receive Django delete signals. Use DB/Python variants consistently along a chain of model references (`DO_NOTHING` is exempt); run system checks and review migrations before switching. `DB_SET_DEFAULT` requires `db_default`, not merely a Python `default`.

`JSONNull` (6.1) for JSON scalar `null` vs SQL `NULL`. Don’t use `None` as top-level JSON null in new queries.

---

## 4. QuerySet — the interview core

```python
# Get / create
from decimal import Decimal
from django.db import transaction
from django.db.models import Prefetch, F, Value

o = Order.objects.get(pk=1)                 # DoesNotExist / MultipleObjectsReturned
o = Order.objects.filter(status="open").first()
o = Order.objects.create(user=u, total=Decimal("0.00"))
# get_or_create() is race-safe only when lookup fields have DB uniqueness.
# user is NOT unique on Order: a user can own many orders.

# Spanning relations
Order.objects.filter(user__email__iexact="a@x.com")
Order.objects.filter(user__in=User.objects.filter(is_active=True))

# Avoid N+1
Order.objects.select_related("user")        # FK / O2O — JOIN
Order.objects.prefetch_related("items")     # M2M / reverse FK — 2nd query
Order.objects.prefetch_related(
    Prefetch("items", queryset=Item.objects.filter(active=True), to_attr="active_items")
)

# 6.1 fetch modes — on-demand field load policy
from django.db import models as m
qs = Order.objects.fetch_mode(m.FETCH_PEERS)   # accessing .user on one instance loads peers too
qs = Order.objects.fetch_mode(m.FETCH_RAISE)   # touching deferred/unfetched field raises

# Aggregation
from django.db.models import Count, Sum, Q, F, Value
from django.db.models.functions import Coalesce
Order.objects.values("status").annotate(n=Count("id"), revenue=Sum("total"))
Order.objects.filter(total__gt=F("user__credit_limit"))
Order.objects.update(total=F("total") * Value(Decimal("1.10")))  # numeric, not text

# Existence
if Order.objects.filter(user=u, status="open").exists():
    ...

# Bulk
Order.objects.bulk_create([Order(user=u, total=1) for _ in range(100)], batch_size=500)
Order.objects.filter(status="open").update(status="paid")   # no save(), no auto_now
Order.objects.filter(pk__in=ids).delete()                   # can be slow; consider DB_CASCADE

# Locking
with transaction.atomic():
    o = Order.objects.select_for_update().get(pk=1)
```

**Never** iterate `for o in Order.objects.all()` on a large table — `.iterator(chunk_size=2000)` or paginate.

`only()` / `defer()` for column subsets. `explain()` shows a plan; `explain(analyze=True)` actually executes the query and can acquire locks or run DB-side effects.

---

## 5. Transactions

```python
from django.db import transaction

@transaction.atomic
def pay(order_id):
    o = Order.objects.select_for_update().get(pk=order_id)
    o.status = Order.Status.PAID
    o.save(update_fields=["status"])

# Nested atomic() creates a savepoint inside an outer transaction.
# Catch DB errors OUTSIDE the inner block so rollback repairs the transaction.
from django.db import IntegrityError
with transaction.atomic():
    try:
        with transaction.atomic():
            Order.objects.create(user=u, total=-1)  # violates total_gte_0
    except IntegrityError:
        pass  # outer transaction can still be used
```

Low-level `savepoint_create()` (6.1; formerly `savepoint()`) needs an active transaction. Prefer nested `atomic()`.

`transaction.on_commit(lambda order_id=o.id: queue_job(order_id))` runs after commit so workers do not race the transaction. A callback is not durable delivery: use a transactional outbox if a crash between commit and enqueue must not lose a job.

The `pay()` function above illustrates locking/state persistence only; real payment processing needs ownership checks, verified payment results and idempotency. Do not hold a DB lock across a slow payment-provider request.

---

## 6. URLs and views

```python
# config/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/orders/", include("orders.urls")),
]

# orders/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path("", views.OrderList.as_view(), name="order-list"),
    path("<int:pk>/", views.order_detail, name="order-detail"),
]
```

```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET, require_POST

@login_required
@require_GET
def order_detail(request, pk):
    o = get_object_or_404(Order.objects.select_related("user"), pk=pk, user=request.user)
    return render(request, "orders/detail.html", {"order": o})

# Async view (ASGI)
async def ping(request):
    return JsonResponse({"ok": True})
```

CBV:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

class OrderList(LoginRequiredMixin, ListView):
    paginate_by = 50
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("user")
```

Redirects (6.1): `RedirectView.preserve_request` → 307/308 keep method/body.

---

## 7. Forms

```python
from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["total", "payload"]

    def clean_total(self):
        t = self.cleaned_data["total"]
        if t < 0:
            raise forms.ValidationError("total >= 0")
        return t

@login_required
def create(request):
    form = OrderForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect("order-detail", pk=obj.pk)
    return render(request, "orders/form.html", {"form": form})
```

CSRF: `{% csrf_token %}` in templates; AJAX header `X-CSRFToken`. DRF `SessionAuthentication` enforces CSRF for authenticated unsafe requests. Do not exempt session/cookie authentication merely because the endpoint returns JSON. Authorization-header tokens have different CSRF exposure; cookie-carried JWTs still need CSRF protection.

---

## 8. Templates

```django
{% extends "base.html" %}
{% load static %}
{% block content %}
  <h1>{{ order }}</h1>
  {% for item in order.items.all %}  {# N+1 unless prefetched #}
    {{ item.name }}
  {% empty %}none{% endfor %}
  <img src="{% static 'img/logo.png' %}">
{% endblock %}
```

Auto-escape on. `|safe` is a security decision. `{% url 'order-detail' pk=order.pk %}`.

---

## 9. Admin

```python
from django.contrib import admin

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total", "created_at")
    list_filter = ("status",)
    search_fields = ("user__email",)
    autocomplete_fields = ("user",)
    list_select_related = ("user",)   # 6.1: specify fields, don't use True
    readonly_fields = ("created_at",)
```

Custom user: set `AUTH_USER_MODEL` first, then `createsuperuser`.

---

## 10. Auth

```python
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import make_password

@permission_required("orders.change_order")
def edit(request, pk): ...

request.user.is_authenticated
request.user.has_perm("orders.change_order")
```

Password hashers: PBKDF2 iterations raised again in 6.1 (1.5M). Prefer Argon2 in `PASSWORD_HASHERS` for new projects.

Sessions: DB/cache/cached_db. Don’t store huge blobs. `SESSION_COOKIE_HTTPONLY = True`.

Model permissions do not automatically enforce object ownership. Scope user-facing queries to the caller and check object-specific access where needed.

---

## 11. DRF (typical companion — not Django core)

```python
# pip install djangorestframework
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "status", "total", "created_at")
        read_only_fields = ("id", "status", "created_at")

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        order = self.get_object()  # ownership-scoped lookup + object permissions
        # Delegate verified payment/idempotency to an application service.
        # Do not report success or mark PAID before implementing that workflow.
        return Response({"detail": "Payment workflow not implemented"}, status=501)
```

Add `rest_framework` to `INSTALLED_APPS` and register this viewset with a DRF router. Defaults are session + basic authentication, not JWT; JWT needs a separate integration. Configure pagination and throttling explicitly. N+1: `prefetch_related` in `get_queryset`.

---

## 12. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate orders 0003
```

Data migration:

```python
from django.db import migrations

def forwards(apps, schema_editor):
    Order = apps.get_model("orders", "Order")  # historical model, not app.models
    Order.objects.using(schema_editor.connection.alias).filter(status="Open").update(status="open")

class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]  # replace with actual predecessor
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
```

Never import `from orders.models import Order` in migrations. `noop` does not undo transformed data; choose a real reverse function or an irreversible operation when appropriate.

---

## 13. Signals — use sparingly

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def on_save(sender, instance, created, **kwargs):
    if created:
        ...
```

Signals hide control flow. Prefer service layer calls. **`DB_CASCADE` does not fire delete signals.**

---

## 14. Cache

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}

cache.set("k", value, timeout=60)
cache.get("k")
cache.get_or_set("k", compute, 60)

@cache_page(30)
def hot(request): ...
```

6.1: cache keys that vary on extra args **changed** — expect cold cache after upgrade.

For personalized responses, include the user/tenant and relevant authorization state in the cache strategy; a URL-only shared cache can disclose another user's response. `get_or_set` does not guarantee only one concurrent computation.

---

## 15. Tasks (Django 6.0+ built-in)

```python
from django.tasks import task

@task()
def send_receipt(order_id: int):
    ...

# enqueue after commit
from django.db import transaction
transaction.on_commit(lambda: send_receipt.enqueue(order.id))
```

Backends via `TASKS`. Django supplies the task API, not a production worker engine. The default immediate backend executes inline; a durable queue and worker require a suitable external backend, or a separate Celery/RQ integration.

---

## 16. Testing

```python
from django.test import TestCase, TransactionTestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", email="a@x.com", password="pw")
        self.client.force_login(self.user)

    def test_list(self):
        r = self.client.get(reverse("order-list"))
        self.assertEqual(r.status_code, 200)
        self.assertQuerySetEqual(r.context["object_list"], [])

# pytest-django
# pytest.ini: DJANGO_SETTINGS_MODULE=config.settings.test
# def test_ok(client, django_user_model):
```

`TestCase` wraps each test in a transaction (fast). Tests that need real commits: `TransactionTestCase`. `RequestFactory` for unit-testing views without middleware stack.

`assertNumQueries(2, func)` — catch N+1 in CI.

---

## 17. Security checklist

| Item | Setting / practice |
|---|---|
| XSS | templates auto-escape; `|safe` rare |
| CSRF | middleware + token; SameSite cookies |
| SQL injection | ORM; never f-string SQL; `params=` on extra |
| Host header | `ALLOWED_HOSTS` |
| Clickjacking | `XFrameOptionsMiddleware` |
| HTTPS | `SECURE_*` in prod |
| Secrets | env, not settings committed |
| CSP | configure `SECURE_CSP` + `ContentSecurityPolicyMiddleware`; use `django.template.context_processors.csp` and nonces when needed (6.1 `csp_nonce_attr`) |
| Uploads | validate type/size; don’t serve user files from same origin without care |
| Admin | 2FA, IP allowlist, not at `/admin` on the public host if avoidable |

---

## 18. Performance (say this in interviews)

1. `select_related` / `prefetch_related` / **6.1 `FETCH_PEERS`**
2. `iterator()`, pagination, `exists()` not `len(qs)`
3. `update_fields` on `save()`
4. `CONN_MAX_AGE` for sync deployments; set it to **0 under ASGI** and use backend pooling where appropriate. PgBouncer transaction pooling keeps a connection for an active transaction (so row locks work), but session features and server-side cursors need care.
5. `EXPLAIN ANALYZE`, indexes matching `filter`+`order_by`
6. `defer` huge JSON/text columns
7. cache at the right layer (full page vs fragment vs queryset)
8. `bulk_create` / `bulk_update`
9. Don’t do Python loops of `.save()` 
10. `DEBUG=False` in prod (`django.db.connection.queries` only works in DEBUG)

---

## 19. Async

```python
async def view(request):
    user = await request.auser()          # async auth
    if not user.is_authenticated:
        return JsonResponse({"detail": "Authentication required"}, status=401)
    qs = Order.objects.filter(user_id=user.id)
    orders = [o async for o in qs]
    return JsonResponse({"n": len(orders)})
```

ORM async: `aget`, `acreate`, `asave`, and `async for` over `.filter(...)`; there is **no `afilter()`**. Query-building methods do not execute I/O. Sync ORM evaluation inside an async context raises `SynchronousOnlyOperation`; other blocking calls can stall the loop. Transactions are not supported in async ORM mode: put the entire transactional unit in a synchronous function and call it with `sync_to_async(..., thread_sensitive=True)`.

---

## 20. 6.0 / 6.1 highlights to mention

- **6.0:** Tasks framework, CSP middleware, template partials; `STORAGES` arrived earlier (4.2)
- **6.1:** `fetch_mode` / `FETCH_PEERS`, `DB_CASCADE`, `MAILERS`, UUID7 db function, admin accessibility, calendar versioning (2028)
- **Removed/dropped:** PG 14, MySQL < 8.4, MariaDB < 10.11
- **Deprecated:** `EMAIL_*` settings, `select_related()` with no args, `list_select_related = True`

---

## 21. Commands you’ll actually type

```bash
python manage.py check --deploy
python manage.py makemigrations --dry-run --verbosity 3
python manage.py showmigrations
python manage.py dbshell
python manage.py shell_plus          # django-extensions
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py test --keepdb -v2
```

---

## Review notes and official references

All 17 Python fragments passed syntax checks on Python 3.12. Targeted checks with Django 6.1.1 and DRF 3.18 covered model checks, ownership filtering, form/serializer creation and transaction rollback using SQLite. This does not validate PostgreSQL locking, production services or every partial example as a complete app.

- Version-specific features and deprecations: [Django 6.1 release notes](https://docs.djangoproject.com/en/6.1/releases/6.1/).
- Query and async behavior: [QuerySet reference](https://docs.djangoproject.com/en/6.1/ref/models/querysets/), [async support](https://docs.djangoproject.com/en/6.1/topics/async/).
- Worker/backend responsibilities: [Django tasks](https://docs.djangoproject.com/en/6.1/topics/tasks/).
- Authentication defaults and CSRF: [DRF authentication](https://www.django-rest-framework.org/api-guide/authentication/).
