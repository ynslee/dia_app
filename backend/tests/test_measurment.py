# import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import measurement
# from models.measurement import MeasurementCreate, MeasurementRead
# from models.measurement import MeasurementUpdate, MeasurementType


"""Tests for single measurement API endpoints."""


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
    assert response.status_code == 200
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
