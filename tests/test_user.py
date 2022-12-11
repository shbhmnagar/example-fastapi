from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_create_user(client):
    res = client.post('/users',
                      json={'email': 'test@gmail.com', 'password': 'password'})

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == 'test@gmail.com'


def test_login_user(client, test_create_login_user):

    res = client.post('/login',
                      data={'username': test_create_login_user['email'], 'password': test_create_login_user['password']})

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         key=settings.secret_key, algorithms=settings.algorithm)
    id = payload.get('user_id')

    assert res.status_code == 200
    assert id == test_create_login_user['id']
    assert login_res.token_type == 'bearer'


@pytest.mark.parametrize('email, password, status_code', [
    ('wrong@email.com', 'password', 403),
    ('test@mail.com', 'wrong_password', 403),
    ('wrong@email.com', 'wrong_password', 403),
    (None, 'password', 422),
    ('test@mail.com', None, 422)
])
def test_incorrect_login(client, test_create_login_user, email, password, status_code):

    res = client.post('/login',
                      data={'username': email, 'password': password})

    assert res.status_code == status_code
