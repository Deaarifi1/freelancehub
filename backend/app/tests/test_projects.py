def get_token(client, role="client"):
    email = f"{role}@test.com"
    username = f"{role}user"
    client.post("/auth/register", json={
        "email": email,
        "username": username,
        "password": "test123",
        "role": role
    })
    login = client.post("/auth/login", data={
        "username": username,
        "password": "test123"
    })
    return login.json()["access_token"]

def test_create_project(client):
    token = get_token(client, "client")
    response = client.post(
        "/projects/",
        json={
            "title": "Test Project",
            "description": "Test description",
            "budget_min": 100,
            "budget_max": 500,
            "project_type": "fixed"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Project"

def test_get_projects(client):
    response = client.get("/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_project_not_found(client):
    response = client.get("/projects/999")
    assert response.status_code == 404

def test_update_project(client):
    token = get_token(client, "client")
    create = client.post(
        "/projects/",
        json={
            "title": "Test Project",
            "description": "Test description",
            "budget_min": 100,
            "budget_max": 500,
            "project_type": "fixed"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    project_id = create.json()["id"]
    response = client.put(
        f"/projects/{project_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"