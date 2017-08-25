
import aiohttp
import pytest

pytestmark = pytest.mark.asyncio


async def test_httpbin_fixture_attributes(httpbin):
    assert httpbin.url.startswith("http://localhost")
    assert (httpbin.url / "foobar").endswith("/foobar")
    assert httpbin.host == "localhost"
    assert httpbin.port


async def test_httpbin_is_running(httpbin):
    async with aiohttp.ClientSession() as session:
        async with session.get(httpbin.url / "status/418") as resp:
            assert resp.status == 418
