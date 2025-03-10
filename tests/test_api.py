import pytest
from app.models import User, Role, Project, db
from flask_jwt_extended import create_access_token

# ----------------------------
# Fixtures
# ----------------------------
@pytest.fixture
def admin_token(app):
    """
    Tạo token cho người dùng Admin.
    """
    with app.app_context():
        # Tạo vai trò
        role_admin = Role(name="Admin")
        role_user = Role(name="User")
        db.session.add_all([role_admin, role_user])

        # Tạo người dùng Admin
        admin = User(username="admin", email="admin@example.com", password="password", role=role_admin)
        db.session.add(admin)
        db.session.commit()

        # Tạo token JWT cho Admin
        token = create_access_token(identity={"id": admin.id, "role": "Admin"})
        return token

# ----------------------------
# Test Cases
# ----------------------------
def test_get_projects(client, admin_token):
    """
    Kiểm tra yêu cầu GET đến /api/projects với quyền Admin.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/projects", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_project(client, admin_token):
    """
    Kiểm tra tạo dự án mới với quyền Admin.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    data = {"name": "Test Project", "description": "A test project"}
    response = client.post("/api/projects", json=data, headers=headers)

    assert response.status_code == 201
    assert response.json["message"] == "Project created successfully"

def test_register_user(client):
    """
    Kiểm tra đăng ký người dùng mới.
    """
    data = {"username": "testuser", "email": "testuser@example.com", "password": "password"}
    response = client.post("/register", json=data)

    assert response.status_code == 200
    assert "Account created successfully" in response.json["message"]

def test_create_task(client, admin_token):
    """
    Kiểm tra tạo nhiệm vụ trong một dự án với quyền Admin.
    """
    # Tạo dự án trước
    headers = {"Authorization": f"Bearer {admin_token}"}
    project_data = {"name": "Project for Tasks", "description": "A project to test tasks"}
    project_response = client.post("/api/projects", json=project_data, headers=headers)
    project_id = project_response.json["id"]

    # Tạo nhiệm vụ trong dự án
    task_data = {"name": "Task 1", "description": "First task", "status": "Not Started"}
    response = client.post(f"/api/projects/{project_id}/tasks", json=task_data, headers=headers)

    assert response.status_code == 201
    assert response.json["message"] == "Task created successfully"
