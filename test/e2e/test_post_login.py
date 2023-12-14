from app import app

def test_post_login(test_app):
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    response = test_app.get('/post_login')

    assert b'Welcome back' in response.data

    assert b'Create Post' in response.data

def test_post_login_not_logged_in(test_app):
    response = test_app.post('/logout',follow_redirects=True)

    assert b'Create Post' not in response.data

    response = test_app.get('/post_login')
    
    assert response.status_code == 401