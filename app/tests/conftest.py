import pytest
from views import app, db
from models import User, Post


@pytest.fixture(scope='module')
def test_client():
    app.config.update({
        "TESTING": True,
    })
    yield app.test_client()


@pytest.fixture(scope='module')
def init_database(test_client):
    with app.app_context():
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/TestDb'
        db.create_all()
        user1 = User(username='lol', email='lol@lol.ru', pwd='12345678')
        post1 = Post(title='LolPost', intro='lol', text='xex', user_name=user1.username)
        db.session.add(user1)
        db.session.add(post1)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def login_user(test_client):
    test_client.post('/login',
                     data=dict(email='lol@lol.ru', password='12345678'),
                     follow_redirects=True)
    yield test_client
    test_client.get('/logout', follow_redirects=True)
