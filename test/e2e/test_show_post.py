from app import app
from models import Post

def test_edit_post(test_app):
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    response = test_app.post('/make_post',data={'discussionTitle':'Test','discussionContent':'Test', 'tags' : ['Boss Fight','Strategy']},follow_redirects=True)

    post = Post.query.filter(Post.title == 'Test').first()

    response = test_app.get(f'/posts/{post.id}')

    assert b'Test' in response.data