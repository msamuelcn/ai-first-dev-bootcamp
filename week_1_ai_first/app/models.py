from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    id: int = Field(..., ge=1)
