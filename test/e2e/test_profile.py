from models import User
from app import app

def test_not_logged_in_user_profile(test_app):
    response = test_app.get('/user_profile',follow_redirects=True)
    
    assert response.status_code == 200

    assert b'Login' in response.data

def test_logged_in_user_profile(test_app):

    response = test_app.get('/login')

    assert response.status_code == 200

    assert b'Login' in response.data

    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    assert b'Welcome back' in response.data

    response = test_app.get('/user_profile',follow_redirects=True)

    assert b'Username' in response.data

    assert b'Joined' in response.data

    assert b'Battle Scars' in response.data
    
    assert b'250 Battle Scars Needed' in response.data