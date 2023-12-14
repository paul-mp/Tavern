from app import app

def test_logout(test_app):
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)
    assert b'Welcome back' in response.data
    response = test_app.post('/logout',follow_redirects=True)
    assert b'Create Post' not in response.data
    assert b'Welcome to Tavern' in response.data