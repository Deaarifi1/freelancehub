def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test123",
        "role": "client"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@test.com"
    assert data["username"] == "testuser"
    assert data["role"] == "client"

def test_register_duplicate(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test123",
        "role": "client"
    })
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test123",
        "role": "client"
    })
    assert response.status_code == 400

def test_login_success(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test123",
        "role": "client"
    })
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test123",
        "role": "client"
    })
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_me(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test123",
        "role": "client"
    })
    login = client.post("/auth/login", data={
        "username": "testuser",
        "password": "test123"
    })
    token = login.json()["access_token"]
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"