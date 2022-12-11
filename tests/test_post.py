from app import schemas

def test_get_all_posts(authorized_client, get_test_posts):
    res = authorized_client.get('/posts')
    posts = res.json()
    for post in posts:
        schemas.PostOut(**post)
    assert len(res.json()) == len(get_test_posts)
    assert res.status_code == 200