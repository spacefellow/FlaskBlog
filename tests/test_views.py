def test_main_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_register_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Username' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client, init_database):
    response = test_client.post('/login',
                                data=dict(email='lol@lol.ru', password='1234567890'),
                                follow_redirects=True)
    assert response.status_code == 200
    response = test_client.get('/user_posts')
    assert response.status_code == 200
    response = test_client.get('/create_post')
    assert response.status_code == 200
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

