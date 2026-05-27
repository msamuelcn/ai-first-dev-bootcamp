# AI Interaction Log

## Session 1

Prompt:
"Create a fastapi pydantic model for workout based on the spec.
Include the validation for positive distance and duration."

AI Output:
Implemented a FastAPI + Pydantic workout model in `main.py`

What I Changed:
It needs to be in `models.py` to avoid circular imports.
The directory structure should be:
```week_1_ai_first/
├── app/
│   ├── __init__.py
│   ├── main.py      ← FastAPI app, mounts router
│   ├── models.py    ← WorkoutBase / WorkoutCreate / WorkoutUpdate / Workout
│   └── main.py    ← all 5 CRUD endpoints + in-memory store
├── tests/
│   ├── __init__.py
│   └── test_workouts.py  ← 29 tests
└── requirements.txt
```

Why:
- Avoid circular imports: `main.py` will import from `models.py`, and `models.py` should not import from `main.py`.
- Separation of concerns: `models.py` should only contain data models, while `main.py

---

## Session 2

Prompt:
"Create a FastAPI Pydantic model for Workout based on the spec.
Create the API endpoints based on the spec and aligns with the Pydantic model. Include the validation for create and update for positive distance and duration.
Create tests with pytest to every endpoints. Ensure every scerios should be handled well."

AI Output:
Creating all package init files, models, routes, main, tests, and requirements in one batch since they are all independent:

Issue:
I should not let AI generate all files in one batch. I should have done it step by step to ensure the structure is correct and avoid mistakes.

What I Changed:
- Created `__init__.py` files in `app/` and `tests/` to make them packages.
- Moved the Workout Pydantic models to `models.py`.
- Created `main.py` with all CRUD endpoints and in-memory store.
- Updated `main.py` to import from `models.py` and include the router from `main.py`.

Why:
- First, I need to implement step by step to ensure the structure is correct and avoid mistakes.
- Proper package structure: `__init__.py` files are needed to make directories into packages

---

## Session 3

Prompt:
"Create Pydantic model for Workout based on SPEC.md. Include validation."

AI Output:
Created `models.py` with WorkoutBase, WorkoutCreate, WorkoutUpdate, and Workout models, including validation for positive distance and duration.

---

## Session 4
Prompt:
"Implement POST /workouts using FastAPI. Follow SPEC.md exactly."

AI Output:
Implemented POST /workouts endpoint in `main.py` to create a new workout, following the specifications in SPEC.md.

---

## Session 5
Prompt:
"then Implement GET /workouts and /workouts/{id} using FastAPI. Follow SPEC.md exactly."

AI Output:
Implemented GET /workouts and GET /workouts/{id} endpoints in `main.py` to retrieve all workouts and a specific workout by ID, following the specifications in SPEC.md.


---
## Session 6
Prompt:
"then Implement PUT /workouts/{id} using FastAPI. Follow SPEC.md exactly."

AI Output:
Implemented PUT /workouts/{id} endpoint in `main.py` to update an existing workout by ID, following the specifications in SPEC.md.

---
## Session 7

Prompt:
"then Implement DELETE /workouts/{id} using FastAPI. Follow SPEC.md exactly."
AI Output:
Implemented DELETE /workouts/{id} endpoint in `main.py` to delete a workout by ID, following the specifications in SPEC.md.

---

## Session 8
Prompt:
"Implement Test requirements on every endpoints. Follow SPEC.md exactly."

AI Output:
Created `test_workouts.py` with 29 tests covering all endpoints and scenarios, following the specifications in SPEC.md.

---
## Session 9
Prompt:
how to run this with fast api?

AI Output:
To run the FastAPI application, you can use the following command in your terminal:

```bash
uvicorn app.main:app --reload
```

Issue:
I'll deploy it in Render, the current main.py has no open port specified, and Render requires the app to listen on port 10000.

What I Changed:
Updated `main.py` to include the following code at the bottom to specify the port for Render:

```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
```

Why:
This allows the application to listen on the port specified by the environment variable `PORT`, which is required by Render. If `PORT` is not set, it defaults to 10000. This ensures that the application can run both locally and in the Render environment without modification.

---
## Session 10
Prompt:
"How to run tests with pytest?"

AI Output:
To run the tests with pytest, you can use the following command in your terminal:
```bash
pytest tests/
```

This command will discover and run all the test files in the `tests/` directory.

---
## Session 11
Prompt:
please ignore all python cache in all sprints how?
AI Output:
To ignore all Python cache files in all sprints, you can create a `.gitignore` file in the root directory of your project and add the following lines to it:

```
# Ignore Python cache files
__pycache__/
*.pyc
*.pyo
# Ignore virtual environment
.venv/
```