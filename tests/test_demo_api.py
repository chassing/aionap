import aionap
import pytest

pytestmark = pytest.mark.asyncio


@pytest.fixture
def demo_url():
    return 'https://jsonplaceholder.typicode.com'


async def test_list_user(demo_url):
    async with aionap.API(demo_url) as demo:
        users = await demo.users.get()

    user = users[0]
    assert user['name'] == 'Leanne Graham'
    assert user['username'] == 'Bret'


async def test_new_post(demo_url):
    details = {
        'title': 'A post entry about the life',
        'body': 'Hi. I want to talk about the life and the universe ...',
        'userId': 1
    }
    async with aionap.API(demo_url) as demo:
        post = await demo.posts.post(data=details)
    assert post['id']
    assert post['userId'] == 1


async def test_update_post(demo_url):
    async with aionap.API(demo_url) as demo:
        post = await demo.posts(1).get()
        assert post['title']

        # update post
        details = {'title': post['title'] * 2}
        post = await demo.posts(1).put(data=details)
        assert post['title'] == details['title']
