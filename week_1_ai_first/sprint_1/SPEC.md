# Workout Tracker API Spec

## Objective

Build a REST API for tracking running workouts.

The API should allow users to:
- create workouts
- view workouts
- update workouts
- delete workouts

---

## Tech Stack

- FastAPI
- Pydantic
- Pytest
- Uvicorn

---

## Data Model

Workout

Fields:
- id (integer)
- workout_type (string)
- distance_km (float)
- duration_minutes (integer)
- workout_date (date)

Example:

{
  "id": 1,
  "workout_type": "Long Run",
  "distance_km": 18.5,
  "duration_minutes": 120,
  "workout_date": "2026-05-25"
}

---

## Validation Rules

- workout_type is required
- distance_km must be greater than 0
- duration_minutes must be greater than 0
- workout_date must be valid date

---

## API Endpoints

### POST /workouts

Creates new workout.

Success:
- 201 Created

Errors:
- 400 Invalid payload

---

### GET /workouts

Returns all workouts.

Success:
- 200 OK

---

### GET /workouts/{id}

Returns single workout.

Success:
- 200 OK

Errors:
- 404 Not Found

---

### PUT /workouts/{id}

Updates workout.

Success:
- 200 OK

Errors:
- 404 Not Found
- 400 Invalid payload

---

### DELETE /workouts/{id}

Deletes workout.

Success:
- 200 OK

Errors:
- 404 Not Found

---

## Testing Requirements

- Test all endpoints
- Test invalid payloads
- Test missing records
- Test validation errors

---

## Deployment

Deploy publicly using Render or Railway.

---

## Non-Functional Requirements

- Clean JSON responses
- Proper HTTP status codes
- Readable code
- Modular structure


## The Folder structure should be as follows:
```
week_1_ai_first/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│
├── tests/
│   ├── test_workouts.py
│
├── SPEC.md
├── requirements.txt
├── README.md
```
