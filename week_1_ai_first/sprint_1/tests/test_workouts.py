from fastapi.testclient import TestClient

import week_1_ai_first.sprint_1.app.main as main_module

client = TestClient(main_module.app)

VALID_PAYLOAD = {
    "workout_type": "Long Run",
    "distance_km": 18.5,
    "duration_minutes": 120,
    "workout_date": "2026-05-25",
}


def _create_workout(payload: dict | None = None) -> dict:
    response = client.post("/workouts", json=payload or VALID_PAYLOAD)
    assert response.status_code == 201
    return response.json()


def setup_function() -> None:
    """Reset in-memory storage before each test to keep tests isolated."""
    main_module.workouts.clear()
    main_module.next_id = 1


# POST /workouts


def test_create_workout_returns_201_and_payload() -> None:
    response = client.post("/workouts", json=VALID_PAYLOAD)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "workout_type": "Long Run",
        "distance_km": 18.5,
        "duration_minutes": 120,
        "workout_date": "2026-05-25",
    }


def test_create_workout_invalid_payload_returns_400() -> None:
    payload = {**VALID_PAYLOAD, "distance_km": 0}

    response = client.post("/workouts", json=payload)

    assert response.status_code == 400


# GET /workouts


def test_list_workouts_returns_200_with_all_workouts() -> None:
    _create_workout()
    _create_workout({**VALID_PAYLOAD, "workout_type": "Tempo Run"})

    response = client.get("/workouts")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["id"] == 1
    assert body[1]["id"] == 2


def test_list_workouts_returns_empty_list_when_none_exist() -> None:
    response = client.get("/workouts")

    assert response.status_code == 200
    assert response.json() == []


# GET /workouts/{id}


def test_get_workout_by_id_returns_200() -> None:
    created = _create_workout()

    response = client.get(f"/workouts/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_workout_by_id_returns_404_when_missing() -> None:
    response = client.get("/workouts/999")

    assert response.status_code == 404


# PUT /workouts/{id}


def test_update_workout_returns_200_and_updated_payload() -> None:
    created = _create_workout()
    payload = {**VALID_PAYLOAD, "workout_type": "Intervals", "distance_km": 10.0}

    response = client.put(f"/workouts/{created['id']}", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "id": created["id"],
        "workout_type": "Intervals",
        "distance_km": 10.0,
        "duration_minutes": 120,
        "workout_date": "2026-05-25",
    }


def test_update_workout_returns_404_when_missing() -> None:
    response = client.put("/workouts/999", json=VALID_PAYLOAD)

    assert response.status_code == 404


def test_update_workout_invalid_payload_returns_400() -> None:
    created = _create_workout()
    payload = {**VALID_PAYLOAD, "duration_minutes": 0}

    response = client.put(f"/workouts/{created['id']}", json=payload)

    assert response.status_code == 400


# DELETE /workouts/{id}


def test_delete_workout_returns_200() -> None:
    created = _create_workout()

    response = client.delete(f"/workouts/{created['id']}")

    assert response.status_code == 200
    assert response.json() == {"message": "Workout deleted successfully"}


def test_delete_workout_returns_404_when_missing() -> None:
    response = client.delete("/workouts/999")

    assert response.status_code == 404


# Validation rules


def test_validation_workout_type_required() -> None:
    payload = {
        "distance_km": 5.0,
        "duration_minutes": 30,
        "workout_date": "2026-05-25",
    }

    response = client.post("/workouts", json=payload)

    assert response.status_code == 400


def test_validation_distance_must_be_positive() -> None:
    response = client.post("/workouts", json={**VALID_PAYLOAD, "distance_km": -1.0})

    assert response.status_code == 400


def test_validation_duration_must_be_positive() -> None:
    response = client.post("/workouts", json={**VALID_PAYLOAD, "duration_minutes": -1})

    assert response.status_code == 400


def test_validation_workout_date_must_be_valid() -> None:
    response = client.post(
        "/workouts", json={**VALID_PAYLOAD, "workout_date": "bad-date"}
    )

    assert response.status_code == 400
