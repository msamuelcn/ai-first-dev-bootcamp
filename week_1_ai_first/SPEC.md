# Workout Tracker API Spec

## Objective
Create a REST API for tracking running workouts.

---

## Technology
- FastAPI
- Pydantic
- Pytest

---

## Workout Model

Fields:
- id: integer
- workout_type: string
- distance_km: float
- duration_minutes: integer
- workout_date: date

---

## Endpoints

### POST /workouts
Create new workout.

Validation:
- workout_type required
- distance_km > 0
- duration_minutes > 0

Returns:
- 201 Created
- created workout object

---

### GET /workouts
Returns all workouts.

---

### GET /workouts/{id}
Returns single workout referenced by the ID.

Errors:
- 404 if not found

---

### PUT /workouts/{id}
Updates workout referenced by the ID.

Validation same as create.

---

### DELETE /workouts/{id}
Deletes workout referenced by the ID.

Returns:
- success message

---

## Testing Requirements
- Test all endpoints
- Test invalid payloads
- Test missing records

---

## Deployment
Deploy publicly using Render.
