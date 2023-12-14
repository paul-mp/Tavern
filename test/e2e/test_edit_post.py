from app import app
from models import Post

def test_edit_post(test_app):
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    post = Post.query.filter(Post.title == 'test').first()

    if post:
        post_id = post.id

    response = test_app.post('/edit_post/{post_id}',data={'discussionTitle':'Test1','discussionContent':'Test1'},follow_redirects=True)

    assert b'Test' not in response.data

    assert b'Test1' in response.data