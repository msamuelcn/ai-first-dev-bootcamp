from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import os
import uvicorn

from week_1_ai_first.sprint_1.app.models import Workout, WorkoutCreate, WorkoutUpdate

app = FastAPI(title="Workout Tracker API")

# In-memory store for workouts.
workouts: dict[int, Workout] = {}
next_id = 1


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


@app.post("/workouts", response_model=Workout, status_code=status.HTTP_201_CREATED)
def create_workout(payload: WorkoutCreate) -> Workout:
    global next_id

    created = Workout(id=next_id, **payload.model_dump())
    workouts[next_id] = created
    next_id += 1
    return created


@app.get("/workouts", response_model=list[Workout], status_code=status.HTTP_200_OK)
def list_workouts() -> list[Workout]:
    return list(workouts.values())


@app.get("/workouts/{id}", response_model=Workout, status_code=status.HTTP_200_OK)
def get_workout(id: int) -> Workout:
    workout = workouts.get(id)
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found",
        )
    return workout


@app.put("/workouts/{id}", response_model=Workout, status_code=status.HTTP_200_OK)
def update_workout(id: int, payload: WorkoutUpdate) -> Workout:
    existing = workouts.get(id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found",
        )

    updated = Workout(id=id, **payload.model_dump())
    workouts[id] = updated
    return updated


@app.delete("/workouts/{id}", status_code=status.HTTP_200_OK)
def delete_workout(id: int) -> dict[str, str]:
    workout = workouts.get(id)
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found",
        )

    del workouts[id]
    return {"message": "Workout deleted successfully"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
