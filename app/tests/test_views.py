def test_main_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_register_page(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'Username' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client, init_database):
    response = test_client.post('/login',
                                data=dict(email='lol@lol.ru', password='12345678'),
                                follow_redirects=True)
    assert response.status_code == 200
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200


def test_create_post(login_user, init_database):
    response = login_user.post('/create_post',
                               data=dict(title='123', intro='123', text='123'),
                               follow_redirects=True)
    assert response.status_code == 200


def test_update_post(login_user, init_database):
    response = login_user.post('/user_posts/1/update',
                               data=dict(title='12344', intro='123', text='xAxa'),
                               follow_redirects=True)
    assert response.status_code == 200


def test_delete_post(login_user, init_database):
    response = login_user.delete('/user_posts/1/delete',
                                 data=dict(title='12344', intro='123', text='xAxa'),
                                 follow_redirects=True)
    assert response.status_code == 200


def test_login_required(test_client):
    response = test_client.get('/user_posts')
    assert response.status_code == 302
    response = test_client.get('/create_post')
    assert response.status_code == 302


def test_post_detail(test_client, init_database):
    response = test_client.get('/1')
    assert response.status_code == 200
    assert b'LolPost' in response.data
    assert b'lol' in response.data
    assert b'xex' in response.data
