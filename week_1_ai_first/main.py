from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Workout Tracker API")


class WorkoutBase(BaseModel):
    workout_type: str = Field(..., min_length=1)
    distance_km: float = Field(..., gt=0)
    duration_minutes: int = Field(..., gt=0)
    workout_date: date


class WorkoutCreate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    id: int


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
