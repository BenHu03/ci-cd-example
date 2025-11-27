# test.py
import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_read_main(client):
    """
    Test the root endpoint returns 200 and correct structure.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "1.0.0"}

def test_addition_logic(client):
    """
    Test the math endpoint to ensure logic holds.
    """
    response = client.get("/add/5/10")
    assert response.status_code == 200
    assert response.get_json() == {"result": 15}
    
def test_invalid_input(client):
    """
    Test that sending text instead of integers results in 404 (Flask behavior).
    """
    response = client.get("/add/five/ten")
    # Flask returns 404 if the route type <int:> doesn't match, unlike FastAPI's 422
    assert response.status_code == 404

def test_login_valid(client):
    """
    Test login with valid credentials.
    """
    response = client.post('/login', json={'username': 'user1', 'password': 'pass1'})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Login successful"}

def test_login_invalid(client):
    """
    Test login with invalid credentials.
    """
    response = client.post('/login', json={'username': 'user1', 'password': 'wrong'})
    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid credentials"}

def test_subtract_with_login(client):
    """
    Test subtract function after login.
    """
    # First login
    client.post('/login', json={'username': 'user1', 'password': 'pass1'})
    response = client.get('/subtract/10/5')
    assert response.status_code == 200
    assert response.get_json() == {"result": 5}

def test_subtract_without_login(client):
    """
    Test subtract function without login.
    """
    response = client.get('/subtract/10/5')
    assert response.status_code == 401
    assert response.get_json() == {"message": "Login required"}
