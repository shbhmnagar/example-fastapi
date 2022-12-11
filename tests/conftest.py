from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
import pytest
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'''postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:
                              {settings.database_port}/{settings.database_name}_test'''


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture()
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_create_login_user(client):
    user_data = {
        'email': 'test@mail.com',
        'password': 'password'
    }
    res = client.post('/users', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_create_login_user):
    return create_access_token({'user_id': test_create_login_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client


@pytest.fixture
def get_test_posts(test_create_login_user, session):
    post_data = [
        {'title': 'title 1', 'content': 'content 1',
            'user_id': test_create_login_user['id']},
        {'title': 'title 2', 'content': 'content 2',
            'user_id': test_create_login_user['id']},
        {'title': 'title 3', 'content': 'content 3',
            'user_id': test_create_login_user['id']}
    ]

    session.add_all(map(lambda x: models.Post(**x), post_data))
    session.commit()

    posts = session.query(models.Post).all()

    return posts