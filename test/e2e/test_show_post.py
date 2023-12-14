from app import app
from models import Post

def test_edit_post(test_app):
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    post = Post.query.filter(Post.title == 'test1').first()

    if post:
        post_id = post.id

    response = test_app.post('/posts/{post_id}')

    assert b'Test1' in response.data