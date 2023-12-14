from models import User
from app import app

def test_sign_up(test_app):
    User.query.filter(User.username=='test_user10').delete()

    response = test_app.get('/signup')

    assert response.status_code == 200

    assert b'Create Your Adventurer' in response.data

    response = test_app.post('/signup',data={'username':'test_user10','password':'abc190'},follow_redirects=True)
    test_user = User.query.filter_by(username='test_user10').all()
    assert len(test_user) == 1

    assert b'Login' in response.data


def test_sign_up_user_exist(test_app):
    response = test_app.get('/signup')

    assert response.status_code == 200

    assert b'Create Your Adventurer' in response.data

    response = test_app.post('/signup',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    assert b'Create Your Adventurer' in response.data
    
    assert b'Username already exists.' in response.data

    


