"""
Module 6 Project — AI Dashboard  (STARTER)
API Client
============
Centralised functions for all backend communication.

All API calls should go through these functions so that:
    • The Authorization header is added in one place
    • Error handling is consistent
    • The rest of the app stays clean

Functions to implement:
    login(username, password)   → (token: str | None, error: str | None)
    get_tasks(token)            → (tasks: list | None, error: str | None)
    create_task(token, title)   → (task: dict | None, error: str | None)
    complete_task(token, task_id) → (task: dict | None, error: str | None)
"""

import requests

API_BASE = "http://localhost:8000"


def login(username: str, password: str):
    """
    POST /auth/token with username and password.
    Returns (access_token, None) on success or (None, error_message) on failure.

    TODO: Implement this function.
    Steps:
      1. requests.post(API_BASE + "/auth/token", data={...})
         NOTE: If you're using your own Module 5 API (Option A, recommended),
         this endpoint expects form-encoded data (OAuth2PasswordRequestForm),
         not JSON — use `data=`, not `json=`, or you'll get a 422 error.
         Using the Lesson 11 demo backend instead (Option B)? That one expects
         a JSON body, so use `json=` there.
      2. Check response.ok — if not, return (None, error message)
      3. Parse response.json() — return the access_token
      4. Catch requests.ConnectionError
    """
    # TODO: implement
    #return None, "Not implemented yet"

    try:
        response = requests.post(
            API_BASE + "/auth/token",
            data={
                "username": username,
                "password": password
            }
        )

        if not response.ok:
            return None, f"Login failed: {response.status_code}"

        data = response.json()

        return data.get("access_token"), None

    except requests.ConnectionError:
        return None, "Could not connect to the API."



def get_tasks(token: str):
    """
    GET /tasks with Bearer token.
    Returns (list_of_tasks, None) or (None, error_message).

    TODO: Implement this function.
    Include the header: {"Authorization": f"Bearer {token}"}
    """
    # TODO: implement
    #return None, "Not implemented yet"

    try:
        response = requests.get(
            API_BASE + "/tasks",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        if not response.ok:
            return None, f"Could not load tasks: {response.status_code}"

        return response.json(), None

    except requests.ConnectionError:
        return None, "Could not connect to the API."


def create_task(token: str, title: str):
    """
    POST /tasks with Bearer token and JSON body {"title": title}.
    Returns (new_task_dict, None) or (None, error_message).

    TODO: Implement this function.
    """
    # TODO: implement
    #return None, "Not implemented yet"
    try:
        response = requests.post(
            API_BASE + "/tasks",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "title": title
            }
        )

        if not response.ok:
            return None, f"Could not create task: {response.status_code}"

        return response.json(), None

    except requests.ConnectionError:
        return None, "Could not connect to the API."


def complete_task(token: str, task_id: int):
    """
    PATCH /tasks/{task_id} with Bearer token and JSON body {"completed": True}.
    Returns (updated_task_dict, None) or (None, error_message).

    TODO: Implement this function.
    NOTE: Your own Module 5 API (Option A, recommended) almost certainly has no
    dedicated "/complete" route — it uses this generic PATCH endpoint for partial
    updates instead. The Lesson 11 demo backend (Option B) is the one with a
    dedicated PATCH /tasks/{task_id}/complete route; adjust the URL below if
    you're using that backend instead.
    """
    # TODO: implement
    #return None, "Not implemented yet"
    try:
        response = requests.patch(
            API_BASE + f"/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        if not response.ok:
            return None, f"Could not complete task: {response.status_code}"

        return response.json(), None

    except requests.ConnectionError:
        return None, "Could not connect to the API."

def get_ai_response(token: str, prompt: str):
    """
    Get an AI response.
    """
    return "This is a test AI response."    