def test_get_threads(client):
    headers = {
        "x-request-id": "123456789",
    }

    response = client.get("/api/v1/threads", headers=headers)
    print("response:", response.json())

    response_data = response.json()

    assert response.status_code == 200

    assert response_data, "Response is empty"

    # Take first thread in the response
    thread = response_data[0]

    # Assert against the attributes of the thread object
    assert "thread_id" in thread, "Thread ID attribute missing"
    assert "consumer_id" in thread, "Consumer ID attribute missing"
    assert "user_id" in thread, "User ID attribute missing"
    assert "status" in thread, "Status attribute missing"
    assert "created_on" in thread, "Created on attribute missing"
    assert "modified_on" in thread, "Modified on attribute missing"
    assert "messages" in thread, "Messages attribute missing"

    # Take first message from the thread's messages array
    message = thread["messages"][0]

    # Assert against the attributes of the message object
    assert "query" in message, "Query attribute missing"
    assert "answer" in message, "Answer attribute missing"
    assert "created_on" in message, "Message Created on attribute missing"
    assert "sources" in message, "Sources attribute missing"

    # Take first source from the sources array
    source = message["sources"][0]

    # Assert against the attributes of the source object
    assert "title" in source, "Source Title attribute missing"
    assert "url" in source, "Source URL attribute missing"
    assert "created_on" in source, "Source Created on attribute missing"


def test_get_thread_by_thread_id(client):
    headers = {
        "x-request-id": "123456789",
    }

    thread_id = "9462a79e-c207-46e1-8552-17458a83c727"

    # Make the GET request to fetch the specific thread
    response = client.get(f"/api/v1/threads/{thread_id}", headers=headers)

    # Verify the response status code
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}"

    # Verify the response content type
    assert (
        response.headers["Content-Type"] == "application/json"
    ), "Response content type is not JSON"

    # Verify the response body
    thread = response.json()

    # Check if the response is not empty
    assert thread, "Thread response is empty"

    # Verify attributes of the thread
    assert "thread_id" in thread, "Thread ID attribute missing in response"
    assert (
        thread["thread_id"] == thread_id
    ), f"Expected thread_id '{thread_id}' but got '{thread['thread_id']}'"


def test_close_thread_by_thread_id(client):
    headers = {
        "x-request-id": "123456789",
    }

    thread_id = "9462a79e-c207-46e1-8552-17458a83c727"

    # Make the PATCH request to close the specific thread
    response = client.patch(f"/api/v1/threads/{thread_id}/close", headers=headers)

    # Verify the response status code
    assert (
        response.status_code == 204
    ), f"Expected status code 204 but got {response.status_code}"

    # Verify the thread is successfully closed and no content is returned
    assert not response.content, "Unexpected content in response"

    # We can make another request to fetch the thread and verify its status
    thread_response = client.get(f"/api/v1/threads/{thread_id}", headers=headers)
    assert thread_response.status_code == 200, "Failed to fetch thread after closing"
    thread_data = thread_response.json()
    assert "status" in thread_data, "Status attribute missing in thread response"
    assert (
        thread_data["status"] is False
    ), f"Expected status False but got {thread_data['status']}"


def test_text_query(client):
    headers = {
        "x-request-id": "123456789",
    }

    data = {"query": "Test Query", "thread_id": "9462a79e-c207-46e1-8552-17458a83c727"}

    # Make the POST request to the endpoint
    response = client.post("/api/v1/threads/text-query", headers=headers, json=data)

    # Verify the response status code
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}"

    # Verify the response content type
    assert (
        response.headers["Content-Type"] == "application/json"
    ), "Response content type is not JSON"

    # Verify the response body
    response_data = response.json()

    # Check if the response is not empty
    assert response_data, "Response is empty"

    # Verify the keys in the response
    assert "thread_id" in response_data, "Thread ID attribute missing in response"
    assert "response" in response_data, "Response attribute missing in response"
    assert "sources" in response_data, "Sources attribute missing in response"

    # Verify the structure and content of the sources
    sources = response_data["sources"]
    assert isinstance(sources, list), "Sources should be a list"
    for source in sources:
        assert isinstance(source, dict), "Each source should be a dictionary"
        assert "title" in source, "Title attribute missing in source"
        assert isinstance(source["title"], str), "Title should be a string"
        assert "url" in source, "URL attribute missing in source"
        assert isinstance(source["url"], str), "URL should be a string"


def test_image_query(client):
    headers = {
        "x-request-id": "123456789",
    }

    data = {
        "image_url": "https://shorturl.at/fqxN0",
        "query": "Test Query",
        "thread_id": "9462a79e-c207-46e1-8552-17458a83c727",
    }

    # Make the POST request to the endpoint
    response = client.post("/api/v1/threads/image-query", headers=headers, json=data)

    # Verify the response status code
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}"

    # Verify the response content type
    assert (
        response.headers["Content-Type"] == "application/json"
    ), "Response content type is not JSON"

    # Verify the response body
    response_data = response.json()

    # Check if the response is not empty
    assert response_data, "Response is empty"

    # Verify the keys in the response
    assert "thread_id" in response_data, "Thread ID attribute missing in response"
    assert "response" in response_data, "Response attribute missing in response"
    assert "sources" in response_data, "Sources attribute missing in response"

    # Verify the structure and content of the sources
    sources = response_data["sources"]
    assert isinstance(sources, list), "Sources should be a list"
    for source in sources:
        assert isinstance(source, dict), "Each source should be a dictionary"
        assert "title" in source, "Title attribute missing in source"
        assert isinstance(source["title"], str), "Title should be a string"
        assert "url" in source, "URL attribute missing in source"
        assert isinstance(source["url"], str), "URL should be a string"
