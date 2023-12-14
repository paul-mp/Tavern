from app import app
from models import Post

def test_edit_post(test_app):
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    response = test_app.post('/make_post',data={'discussionTitle':'Test','discussionContent':'Test', 'tags' : ['Boss Fight','Strategy']},follow_redirects=True)

    assert response.status_code == 200

    post = Post.query.filter(Post.title == 'Test').first()

    assert post is not None

    response = test_app.post(f'/edit_post/{post.id}',data={'title':'Test1','content':'Test1'},follow_redirects=True)

    assert response.status_code == 200

    assert b'Test1' in response.data
    
    Post.query.filter(Post.title=='Test1').delete()