from models import User
from app import app

def test_login(test_app):
    response = test_app.get('/login')

    assert response.status_code == 200

    assert b'Login' in response.data

    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    assert b'Welcome back' in response.data

def test_unsuccesful_login(test_app):
    response = test_app.get('/login')

    assert response.status_code == 200

    assert b'Login' in response.data

    response = test_app.post('/login',data={'username':'test_user1','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    assert b'Incorrect username or password' in response.data