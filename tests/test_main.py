import sys
import os

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# --- Core Required Tests ---

def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }


def test_add_sheep():
    # Prepare the new sheep data in dictionary format
    new_sheep_data = {
        "id": 7,
        "name": "Barnaby",
        "breed": "Suffolk",
        "sex": "ram"
    }

    # Send POST request to endpoint "/sheep/"
    response = client.post("/sheep/", json=new_sheep_data)

    # Assert response status code is 201 (Created)
    assert response.status_code == 201

    # Assert response JSON matches input data
    assert response.json() == new_sheep_data

    # Verify retrieval from database by ID
    get_response = client.get("/sheep/7")
    assert get_response.status_code == 200
    assert get_response.json() == new_sheep_data


# --- Extra Credit Tests ---

def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 6


def test_update_sheep():
    updated_data = {
        "id": 1,
        "name": "Spice the Great",
        "breed": "Gotland",
        "sex": "ewe"
    }
    response = client.put("/sheep/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data

    # Verify persistence
    get_response = client.get("/sheep/1")
    assert get_response.json() == updated_data


def test_delete_sheep():
    # Delete sheep ID 2
    response = client.delete("/sheep/2")
    assert response.status_code == 204

    # Confirm sheep no longer exists (404)
    get_response = client.get("/sheep/2")
    assert get_response.status_code == 404