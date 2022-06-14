import pytest
from config import create_app, db
from models import User, Post


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture(scope='module')
def test_client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()
    user1 = User(username='lol', email='lol@lol.ru', pwd='1234567890')
    post1 = Post(title='LolPost', intro='lol', text='xex', user_name=user1.username)
    db.session.add(user1)
    db.session.add(post1)
    db.session.commit()
    yield db
    db.drop_all()
