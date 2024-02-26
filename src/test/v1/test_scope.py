from fastapi import status

from src.apis.v1.models.scope import ScopeResponse
from src.core.config.settings import settings


scopes_data: list[ScopeResponse] = [
    {"name": "Admin", "description": "Admin Test", "status": True},
    {"name": "Member", "description": "Member Test", "status": True},
    {"name": "Guest", "description": "Guest Test", "status": True},
]

api_route = settings.API_PREFIX + settings.CURRENT_API_VERSION + "/scope"


def test_read_scopes(client):
    response = client.get(api_route)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Admin"
    assert data[1]["name"] == "Member"


def test_read_single_scope(client):
    response = client.get(f"{api_route}/2")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Member"


def test_add_scope(client):
    response = client.post(
        api_route, json={"name": "Visitor", "description": "Visitor Guest"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Visitor"
    assert data["status"] is True
    assert "id" in data
    scope_id = data["id"]

    response = client.get(f"{api_route}/{scope_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Visitor"
    assert data["id"] == scope_id


def test_update_scope(client):
    data = scopes_data[0]
    response = client.put(
        api_route + "/1",
        json={
            "name": data["name"],
            "description": data["description"],
            "status": False,
        },
    )
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    scope_id = data["id"]

    response = client.get(f"{api_route}/{scope_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] is False
    assert data["id"] == scope_id


def test_update_scope_not_found(client):
    response = client.put(api_route + "/500", json=scopes_data[0])
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "No Scope found"}


def test_delete_scope(client):
    response = client.delete(api_route + "/1")
    assert response.status_code == 204


def test_delete_scope_not_found(client):
    response = client.delete(api_route + "/500")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "No Scope found"}
