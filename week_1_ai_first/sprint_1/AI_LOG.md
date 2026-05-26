# AI Interaction Log

## Session 1

Prompt:
"Generate FastAPI model for Workout with validation."

AI Output:
Generated model using BaseModel.

What I Changed:
Added validation for positive values using Field(gt=0).

Why:
Prevent invalid workout distances.

---

## Session 2

Prompt:
"Generate GET endpoint for workouts."

Issue:
AI forgot 404 handling.

What I Changed:
Added HTTPException for missing workout.
