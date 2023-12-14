from models import User
from app import app
from models import Post
from models import Reply

def test_delete_post(test_app):
    Reply.query.filter(Reply.content=='Test').delete()
    Post.query.filter(Post.title=='Test').delete()
    Post.query.filter(Post.title=='Test1').delete()
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    assert b'Welcome back' in response.data

    response = test_app.post('/make_post',data={'discussionTitle':'Test','discussionContent':'Test', 'tags' : ['Boss Fight','Strategy']},follow_redirects=True)

    assert b'Test' in response.data

    post = Post.query.filter(Post.title == 'Test').first()

    response = test_app.post(f'/delete_post/{post.id}',follow_redirects=True)

    assert b'Test' not in response.data