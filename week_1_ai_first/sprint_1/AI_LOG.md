# AI Interaction Log

This file documents major AI-assisted development decisions for Sprint 1.

## Session 1
### Prompt
"Create a FastAPI Pydantic model for workout based on the spec. Include the validation for positive distance and duration."

### AI Output (Summary)
Initial model implementation was suggested in `main.py`.

### Actions Taken
- Moved model definitions to `models.py` to avoid circular imports.
- Clarified target structure:

```text
week_1_ai_first/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app and CRUD endpoints
│   └── models.py       # WorkoutBase / WorkoutCreate / WorkoutUpdate / Workout
├── tests/
│   ├── __init__.py
│   └── test_workouts.py
└── requirements.txt
```

### Why
- Prevent circular imports between API and models.
- Keep separation of concerns: data models in `models.py`, API logic in `main.py`.

---

## Session 2
### Prompt
"Create a FastAPI Pydantic model for Workout based on the spec. Create the API endpoints based on the spec and align with the Pydantic model. Include validation for create and update for positive distance and duration. Create tests with pytest for every endpoint. Ensure every scenario is handled well."

### AI Output (Summary)
Suggested generating all files in one batch.

### Issue Noted
Generating everything at once reduced review quality and increased risk of structural mistakes.

### Actions Taken
- Created `__init__.py` in `app/` and `tests/`.
- Kept models in `models.py`.
- Implemented CRUD endpoints in `main.py` with in-memory store.
- Updated imports to keep module boundaries clear.

### Why
- Incremental implementation is easier to validate.
- Proper package setup improves import reliability.

---

## Session 3
### Prompt
"Create Pydantic model for Workout based on SPEC.md. Include validation."

### AI Output (Summary)
Implemented `WorkoutBase`, `WorkoutCreate`, `WorkoutUpdate`, and `Workout` with positive-value validation.

### Actions Taken
- Finalized workout models and validation logic in `models.py`.

---

## Session 4
### Prompt
"Implement POST /workouts using FastAPI. Follow SPEC.md exactly."

### AI Output (Summary)
Implemented `POST /workouts` in `main.py`.

### Actions Taken
- Added create endpoint aligned with spec behavior.

---

## Session 5
### Prompt
"Then implement GET /workouts and /workouts/{id} using FastAPI. Follow SPEC.md exactly."

### AI Output (Summary)
Implemented `GET /workouts` and `GET /workouts/{id}` in `main.py`.

### Actions Taken
- Added list and single-item retrieval endpoints.

---

## Session 6
### Prompt
"Then implement PUT /workouts/{id} using FastAPI. Follow SPEC.md exactly."

### AI Output (Summary)
Implemented `PUT /workouts/{id}` in `main.py`.

### Actions Taken
- Added update endpoint with validation.

---

## Session 7
### Prompt
"Then implement DELETE /workouts/{id} using FastAPI. Follow SPEC.md exactly."

### AI Output (Summary)
Implemented `DELETE /workouts/{id}` in `main.py`.

### Actions Taken
- Added delete endpoint and response handling.

---

## Session 8
### Prompt
"Implement test requirements on every endpoint. Follow SPEC.md exactly."

### AI Output (Summary)
Created endpoint coverage tests with pytest.

### Actions Taken
- Added `test_workouts.py` with 29 test cases covering expected scenarios.

---

## Session 9
### Prompt
"How to run this with FastAPI?"

### AI Output (Summary)
Provided `uvicorn app.main:app --reload` for local execution.

### Issue Noted
Render deployment required explicit host/port handling.

### Actions Taken
- Updated `main.py` startup block to use `PORT` environment variable with default `10000`.

```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
```

### Why
- Ensures compatibility for both local runs and Render deployment.

---

## Session 10
### Prompt
"How to run tests with pytest?"

### AI Output (Summary)
Provided the command below:

```bash
pytest tests/
```

### Actions Taken
- Documented standard test execution command.

---

## Session 11
### Prompt
"Please ignore all Python cache in all sprints, how?"

### AI Output (Summary)
Suggested `.gitignore` entries for Python cache and local virtual environments.

### Actions Taken
- Added/recorded ignore patterns:

```text
# Ignore Python cache files
__pycache__/
*.pyc
*.pyo

# Ignore virtual environment
.venv/
```