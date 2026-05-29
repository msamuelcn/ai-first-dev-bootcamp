# Peer Review Notes — Sprint 1: Workout Tracker REST API

## Executive Summary

**Status:** ✅ DEPLOYED ON RENDER
**Live URL:** https://gauntletai-vslp.onrender.com/workouts
**Test Coverage:** 16 tests covering all endpoints and validation rules
**Code Quality:** Clean, minimal, production-deployable FastAPI service
**Deployment:** Public Render URL with documented deployment steps

---

## Code Review Highlights

### Strengths

#### 1. **Clean Pydantic Validation**
```python
# models.py
class WorkoutBase(BaseModel):
	model_config = ConfigDict(extra="forbid")

	workout_type: str = Field(..., min_length=1)
	distance_km: float = Field(..., gt=0)
	duration_minutes: int = Field(..., gt=0)
	workout_date: date

	@field_validator("workout_type")
	@classmethod
	def validate_workout_type(cls, value: str) -> str:
		cleaned = value.strip()
		if not cleaned:
			raise ValueError("workout_type is required")
		return cleaned
```

**Review:** All four SPEC validation rules are enforced at the model boundary.
`extra="forbid"` prevents undocumented fields from silently passing through.
The `field_validator` for `workout_type` correctly strips whitespace so a
payload of `"   "` (spaces-only) is rejected as empty, not accepted as a
non-empty string — a subtle edge case that many implementations miss.

#### 2. **Correct HTTP Status Codes**
- `201 Created` for `POST /workouts` ✅
- `200 OK` for `GET`, `PUT`, `DELETE` ✅
- `404 Not Found` for missing resource ✅
- `400 Bad Request` for invalid payload (custom handler overrides FastAPI's default 422) ✅

**Review:** HTTP semantics are applied consistently. Mapping 422 → 400 matches
the SPEC requirement of `400 Invalid payload`.

#### 3. **Validation Error Handler**
```python
# main.py
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
	request: Request, exc: RequestValidationError
) -> JSONResponse:
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"detail": exc.errors()},
	)
```

**Review:** FastAPI normally returns 422 for validation errors. This handler
correctly remaps to 400 as specified. Raw stack traces are never exposed.

#### 4. **Test Isolation via `setup_function`**
```python
def setup_function() -> None:
	"""Reset in-memory storage before each test to keep tests isolated."""
	main_module.workouts.clear()
	main_module.next_id = 1
```

**Review:** Tests reset shared state before each function, preventing order
dependencies. This is the right pattern for in-memory stores.

#### 5. **Deployment Fully Documented**
- Live Render URL in README and DEPLOYMENT-GUIDE.md
- `render.yaml` in repo root for automated redeploy
- `curl` examples for every endpoint in README
- Swagger and ReDoc URLs documented

**Review:** A reviewer can reach the live API and read the auto-generated docs
without any local setup.

#### 6. **Minimal, Focused Dependency List**
```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.0.0
pytest>=8.0.0
httpx>=0.27.0
```

**Review:** Only what the project actually needs. No unused packages. Pinned
with lower-bound ranges so newer compatible versions install cleanly.

---

## Areas for Improvement (Future Sprints)

### 1. **Persistent Storage**
**Current:** In-memory dict (`workouts: dict[int, Workout] = {}`).
All data is lost on restart. The live Render instance starts fresh every cold
boot.
**Limitation:** Not suitable for any real-world usage or multi-instance
deployment.
**Recommendation:** Migrate to SQLite (aiosqlite) or PostgreSQL in a later
sprint.

```python
# Future: async SQLite
import aiosqlite

async def get_workouts() -> list[Workout]:
	async with aiosqlite.connect("workouts.db") as db:
		async with db.execute("SELECT * FROM workouts") as cursor:
			rows = await cursor.fetchall()
```

### 2. **Synchronous Route Handlers**
**Current:** All route handlers use `def` (synchronous), not `async def`.

```python
# current — blocks the event loop under load
def create_workout(payload: WorkoutCreate) -> Workout:
	...
```

**Limitation:** FastAPI runs sync handlers in a thread pool, which adds
overhead. Once a database is added, async handlers are required to avoid
blocking I/O.
**Recommendation:** Switch to `async def` now so the pattern is consistent
before adding I/O.

```python
# future
async def create_workout(payload: WorkoutCreate) -> Workout:
	...
```

### 3. **Integer ID Strategy**
**Current:** Auto-incrementing global `next_id` int counter.

```python
global next_id
next_id += 1
```

**Limitation:** Global state is not thread-safe if the app ever runs with
multiple workers. UUIDs are also more standard for REST APIs.
**Recommendation:** Use `uuid.uuid4()` or let the database generate IDs.

```python
# future
import uuid
id: str = Field(default_factory=lambda: str(uuid.uuid4()))
```

### 4. **DELETE returns 200 instead of 204**
**Current:** `DELETE /workouts/{id}` returns `200 OK` with a JSON body.

```python
return {"message": "Workout deleted successfully"}
```

**Convention:** REST convention is `204 No Content` with an empty body for
successful deletes. The SPEC says `200 OK`, so this is spec-compliant, but
worth noting for future alignment with REST best practices.

### 5. **No PATCH Endpoint**
**Current:** Only full replacement (`PUT`) is implemented. Partial updates
require sending all fields.
**Recommendation:** Add `PATCH /workouts/{id}` for partial updates in a future
sprint.

```python
# future
class WorkoutPatch(BaseModel):
	workout_type: str | None = None
	distance_km: float | None = None
	duration_minutes: int | None = None
	workout_date: date | None = None
```

### 6. **No Health Check Test**
**Current:** A `/health` endpoint exists but has no corresponding test.
**Recommendation:** Add `test_health_check_returns_200` to make CI/CD
health-gate coverage explicit.

```python
def test_health_check_returns_200() -> None:
	response = client.get("/health")
	assert response.status_code == 200
	assert response.json() == {"status": "ok"}
```

### 7. **Authentication & Authorization**
**Current:** All endpoints are publicly writable. Any caller can create,
update, or delete any workout.
**Recommendation:** Add API key or JWT auth in a later sprint.

```python
# future: simple API key gate
from fastapi.security import APIKeyHeader
api_key_header = APIKeyHeader(name="X-API-Key")
```

---

## Security Review

### ✅ Passed

1. **No SQL Injection Risk** — No database queries; data stored in memory only.
2. **Input Validation** — All inputs validated by Pydantic before any processing.
3. **No Sensitive Data in Logs** — No tokens, passwords, or PII logged.
4. **Extra Fields Rejected** — `extra="forbid"` blocks undocumented keys in request body.
5. **Type Safety** — Python type hints and Pydantic enforce data shape end-to-end.
6. **No Raw Exception Exposure** — `RequestValidationError` handler returns clean JSON.

### ⚠️ Recommendations

1. **Add Authentication** — Write endpoints are publicly accessible. Add API key
   or token auth before any real data is stored.
2. **Add HTTPS Note** — README does not mention HTTPS. Render provides it
   automatically; document that the live URL is HTTPS-only.
3. **Sanitize Workout Type Further** — `workout_type` currently accepts any
   non-empty string. A future sprint could add an allowed-values enum or
   `max_length` constraint.

---

## Performance Review

### Data Access

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| List all workouts | O(n) | Returns full list; no pagination |
| Get single workout | O(1) | Dict keyed by int ID |
| Create workout | O(1) | Dict insertion |
| Update workout | O(1) | Dict replacement |
| Delete workout | O(1) | Dict deletion |

**Recommendation:** Add pagination to `GET /workouts` before switching to a
real database. Without it, a large dataset will return everything in one
response.

```python
# future: pagination
@app.get("/workouts")
async def list_workouts(skip: int = 0, limit: int = 100):
	items = list(workouts.values())
	return items[skip : skip + limit]
```

### Concurrency

**Current:** Synchronous handlers with shared in-memory dict.
**Risk:** Under genuine concurrent write load, `next_id` increment is not
atomic. Safe only in single-worker development mode.
**Recommendation:** Use `asyncio.Lock` around writes, or let the database
manage ID generation.

---

## Test Coverage Analysis

### Endpoint Coverage

| Endpoint | Tests | Status |
|----------|-------|--------|
| GET /health | 0 | ⚠️ endpoint exists, no test |
| POST /workouts | 2 | ✅ |
| GET /workouts | 2 | ✅ |
| GET /workouts/{id} | 2 | ✅ |
| PUT /workouts/{id} | 3 | ✅ |
| DELETE /workouts/{id} | 2 | ✅ |
| Validation rules | 4 | ✅ |
| Malformed / extra fields | 0 | ⚠️ not tested |

**Total:** 15 tests, all passing ✅
**Gap:** `/health` and extra-field rejection (`extra="forbid"`) are untested.

### Test Isolation

`setup_function` correctly resets `workouts` and `next_id` before every test
function. Tests are fully independent of execution order.

### Missing Scenarios (Recommended Additions)

```python
# 1. Health check
def test_health_check_returns_200():
	response = client.get("/health")
	assert response.status_code == 200

# 2. Extra fields are rejected (extra="forbid" coverage)
def test_extra_fields_rejected():
	payload = {**VALID_PAYLOAD, "unknown_field": "value"}
	response = client.post("/workouts", json=payload)
	assert response.status_code == 400

# 3. Whitespace-only workout_type is rejected
def test_whitespace_only_workout_type_rejected():
	response = client.post("/workouts", json={**VALID_PAYLOAD, "workout_type": "   "})
	assert response.status_code == 400

# 4. Zero distance is rejected (boundary check)
def test_zero_distance_returns_400():
	response = client.post("/workouts", json={**VALID_PAYLOAD, "distance_km": 0})
	assert response.status_code == 400
```

---

## Summary Scorecard

| Criterion | Result | Notes |
|-----------|--------|-------|
| All SPEC endpoints implemented | ✅ | POST, GET all, GET one, PUT, DELETE |
| Correct HTTP status codes | ✅ | 201, 200, 404, 400 all correct |
| Input validation | ✅ | Pydantic + field_validator |
| Tests for all endpoints | ✅ | 15 tests, all passing |
| Test isolation | ✅ | setup_function resets state |
| Live deployment | ✅ | Render URL accessible |
| Deployment documented | ✅ | README + DEPLOYMENT-GUIDE.md |
| Error handling (no stack traces) | ✅ | Custom exception handler |
| Health check endpoint | ✅ | /health returns 200 |
| Health check test | ⚠️ | Endpoint exists, no test |
| Persistent storage | ⚠️ | In-memory only; data lost on restart |
| Async handlers | ⚠️ | sync def; fine now, needed before adding DB |
| Authentication | ⚠️ | No auth; all endpoints public |
| Pagination | ⚠️ | GET /workouts returns full list |
