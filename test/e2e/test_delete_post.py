from models import User
from app import app
from models import Post

def test_delete_post(test_app):
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    assert b'Welcome back' in response.data

    response = test_app.post('/make_post',data={'discussionTitle':'Test','discussionContent':'Test', 'tags' : ['Boss Fight','Strategy']},follow_redirects=True)

    assert b'Test' in response.data

    post = Post.query.filter(Post.title == 'test').first()

    if post:
        post_id = post.id

    response = test_app.post('/delete_post/{post_id}',follow_redirects=True)

    assert b'Test' not in response.data