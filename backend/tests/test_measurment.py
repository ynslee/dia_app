"""Tests for single measurement API endpoints."""


import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from routers import measurement
# from models.measurement import (
#     MeasurementCreate,
#     MeasurementRead,
#     MeasurementUpdate,
#     MeasurementType
#     )


def get_client():
    """
    Prepares and returns FastAPI client with measurement router added.
    """
    app = FastAPI(title="Mesurements API")
    app.include_router(measurement.router)
    return TestClient(app)


def test_get_measurement():
    """
    Tests get measurement endpoint.
    """
    client = get_client()
    test_id = 1
    response = client.get(f"/measurement/{test_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
                    "id": 1,
                    "measurement_type": "bp",
                    "value_1": 120,
                    "value_2": 78,
                    "source": "wrist",
                    "note": None,
                    "symptoms": "lightheaded",
                    "time_taken": "2025-11-05T14:29:00Z",
                    "created_at": "2025-11-05T14:30:00Z",
                    "updated_at": None
                    }


@pytest.mark.parametrize(
    "bad_id, status_code",
    [
       (-1, status.HTTP_400_BAD_REQUEST),
       ("a", status.HTTP_422_UNPROCESSABLE_ENTITY),
       ("", status.HTTP_405_METHOD_NOT_ALLOWED),
    ],
)
def test_get_measurement_bad_id(bad_id, status_code):
    client = get_client()
    response = client.get(f"/measurement/{bad_id}")
    assert response.status_code == status_code


def test_post_measurement():
    client = get_client()
    payload = {
        "measurement_type": "bs",
        "value_1": 97,
        "value_2": None,
        "time_taken": "2025-11-05T14:29:00Z",
        "source": "accucheck",
        "note": None,
        "symptoms": None,
        }
    response = client.post(f"/measurement", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] == "2"
    

def test_post_measurement_bad_payload():
    client = get_client()
    payload = {
        "value_1": 97,
        "value_2": None,
        "time_taken": "2025-11-05T14:29:00Z",
        "source": "accucheck",
        "note": None,
        "symptoms": None,
        }
    response = client.post(f"/measurement", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
