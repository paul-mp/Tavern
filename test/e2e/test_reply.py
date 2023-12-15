from app import app
from models import Post
from models import Reply

def test_reply(test_app):
    Reply.query.filter(Reply.content=='Test').delete()
    Post.query.filter(Post.title=='Test').delete()
    Post.query.filter(Post.title=='Test1').delete()
    response = test_app.post('/login',data={'username':'test_user10','password':'abc190'},follow_redirects=True)

    assert response.status_code == 200

    response = test_app.post('/make_post',data={'discussionTitle':'Test','discussionContent':'Test', 'tags' : ['Boss Fight','Strategy']},follow_redirects=True)

    assert response.status_code == 200

    post = Post.query.filter(Post.title == 'Test').first()

    assert post is not None

    response = test_app.post(f'/submit_reply/{post.id}',data={'reply_content':'Test'},follow_redirects=True)

    assert response.status_code == 200

    assert b'our reply has been posted.' in response.data

    Reply.query.filter(Reply.content=='Test').delete()


def test_reply_not_logged_in(test_app):
    response = test_app.post('/logout',follow_redirects=True)

    assert response.status_code == 200

    post = Post.query.filter(Post.title == 'Test').first()

    assert post is not None
    response = test_app.post(f'/submit_reply/{post.id}',follow_redirects=True)
    
    print(response.data)

    assert b'Login.' in response.data
