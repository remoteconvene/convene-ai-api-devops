def test_register_consumer(client):
    data = {"name": "test", "description": "testing"}

    headers = {
        "x-request-id": "123456789",
    }

    response = client.post("/api/v1/consumers", headers=headers, json=data)

    # Verify the response status code
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}"

    # Verify the response content type
    assert (
        response.headers["Content-Type"] == "application/json"
    ), "Response content type is not JSON"

    # Verify the response body
    response_data = response.json()

    # Check if the response is not empty
    assert response_data, "Response body is empty"

    # Verify the attributes of the response
    assert "name" in response_data, "Name attribute missing in response"
    assert (
        response_data["name"] == "test"
    ), f"Expected name 'test' but got '{response_data['name']}'"

    assert "description" in response_data, "Description attribute missing in response"
    assert (
        response_data["description"] == "testing"
    ), f"Expected description 'testing' but got '{response_data['description']}'"

    assert "status" in response_data, "Status attribute missing in response"
    assert (
        response_data["status"] is True
    ), f"Expected status True but got '{response_data['status']}'"
