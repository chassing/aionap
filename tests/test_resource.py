
import aionap
import pytest

pytestmark = pytest.mark.asyncio


async def test_get(httpbin):
    api = aionap.API(httpbin.url)
    assert await api.anything.resource.get()['method'] == 'GET'
