
import pytest

import aiohttp
import aionap

pytestmark = pytest.mark.asyncio


async def test_api_base_url():
    api = aionap.API("http://localhost")
    assert api._store['base_url'] == "http://localhost"
    await api.close()


async def test_api_format():
    api = aionap.API("http://localhost")
    # default json
    assert api._store['format'] == "json"
    await api.close()
    # yaml
    api = aionap.API("http://localhost", format='yaml')
    assert api._store['format'] == "yaml"
    await api.close()


async def test_api_append_slash():
    api = aionap.API("http://localhost")
    # default
    assert not api._store['append_slash']
    await api.close()
    #
    api = aionap.API("http://localhost", append_slash=True)
    assert api._store['append_slash']
    await api.close()


async def test_api_auth():
    api = aionap.API("http://localhost")
    # default
    assert not api._store['session']._default_auth
    await api.close()
    #
    api = aionap.API("http://localhost", auth=('user', 'password'))
    assert isinstance(api._store['session']._default_auth, aiohttp.BasicAuth)
    await api.close()


async def test_api_session_kwargs():
    api = aionap.API("http://localhost")
    # default
    assert not api._store['session']._conn_timeout
    await api.close()
    # set
    api = aionap.API("http://localhost", session_kwargs=dict(conn_timeout=5))
    assert api._store['session']._conn_timeout == 5
    await api.close()
