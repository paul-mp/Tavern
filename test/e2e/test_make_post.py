from app import app

def test_make_post(test_app):
    response = test_app.get('/login')

    assert response.status_code == 200

    assert b'Login' in response.data

    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    assert b'Welcome back' in response.data

    response = test_app.post('/make_post',data={'discussionTitle':'How To Kill the Beholder','discussionContent':'Help me and my group are getting stuck in our campaign againist a beholder, any tips to beat it', 'tags' : ['Boss Fight','Strategy']},follow_redirects=True)

    assert b'How To Kill the Beholder' in response.data