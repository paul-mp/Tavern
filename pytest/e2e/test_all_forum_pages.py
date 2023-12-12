from models import User
from app import app

def test_all_forum(test_app):
    reponse = test_app.get('/forums')
    
    assert reponse.status_code == 200

    assert b'Forum Discussions' in reponse.data