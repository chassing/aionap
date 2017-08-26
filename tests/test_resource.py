
import aionap
import pytest

pytestmark = pytest.mark.asyncio


async def test_plain_methods(httpbin):
    """Just the plain http methods without data, params etc."""
    api = aionap.API(httpbin.url, append_slash=False)
    async with api.anything as resource:
        resp = await resource.get()
        assert resp['method'] == 'GET'
        resp = await resource.post()
        assert resp['method'] == 'POST'
        resp = await resource.patch()
        assert resp['method'] == 'PATCH'
        resp = await resource.put()
        assert resp['method'] == 'PUT'
        resp = await resource.delete()
        assert resp['method'] == 'DELETE'


async def test_params(httpbin):
    """Just the plain http methods without data, params etc."""
    api = aionap.API(httpbin.url, append_slash=False)
    params = {'key': 'value', 'key2': 'value2'}
    async with api.anything as resource:
        resp = await resource.get(**params)
        assert resp['args'] == params
        resp = await resource.post(**params)
        assert resp['args'] == params
        resp = await resource.patch(**params)
        assert resp['args'] == params
        resp = await resource.put(**params)
        assert resp['args'] == params
        resp = await resource.delete(**params)
        assert resp['args'] == params


async def test_deep_nested_resource_urls(httpbin):
    """Test _get_resource and __call__."""
    api = aionap.API(httpbin.url)
    async with api.anything.deep.nested.resource.urls as resource:
        resp = await resource.get()
        assert resp['method'] == 'GET'
        assert resp['url'].endswith('deep/nested/resource/urls')


async def test_deep_nested_resource_urls_with_ids(httpbin):
    """Test _get_resource and __call__."""
    api = aionap.API(httpbin.url)
    async with api.anything.deep(1).nested(1).resource(1).urls(1) as resource:
        resp = await resource.get()
        assert resp['url'].endswith('/deep/1/nested/1/resource/1/urls/1')


async def test_deep_nested_resource_urls_with_name(httpbin):
    """Test _get_resource and __call__."""
    api = aionap.API(httpbin.url)
    async with api.anything.deep("name").nested("name").resource("name").urls("name") as resource:
        resp = await resource.get()
        assert resp['url'].endswith('/deep/name/nested/name/resource/name/urls/name')


async def test_close(httpbin):
    api = aionap.API(httpbin.url)
    resp = await api.anything.resource.get()
    assert resp['method'] == 'GET'
    assert resp['data'] == ''
    await api.close()


async def test_append_slash(httpbin):
    api = aionap.API(httpbin.url, append_slash=True)
    async with api.anything.whatever as resource:
        resp = await resource.get()
    assert resp['url'].endswith('/')


async def test_no_append_slash(httpbin):
    api = aionap.API(httpbin.url, append_slash=False)
    async with api.anything.whatever as resource:
        resp = await resource.get()
        assert not resp['url'].endswith('/')

async def test_default_no_append_slash(httpbin):
    api = aionap.API(httpbin.url)
    async with api.anything.whatever as resource:
        resp = await resource.get()
        assert not resp['url'].endswith('/')


@pytest.mark.parametrize("code", [
    # OK
    200, 201, 202, 203, 204,
    # no redirects
    300, 304,
    # redirects
    301, 302, 303, 307,
    # client error
    400, 401, 402, 403, 404, 405,
    # server error
    500, 501, 502, 503, 505,
])
async def test_all_http_status_codes(httpbin, code):
    """Just the plain http methods without data, params etc."""
    api = aionap.API(httpbin.url)
    async with api.status(code) as resource:
        if 300 <= code <= 399:
            resp = await resource.get()
            if code not in [300, 304]:
                # it's real location: XXX response, therefor test redirection
                code = 200
                # httpbin std redirect is to /get
                assert resp['url'].endswith('/get')
        elif 400 <= code <= 499:
            with pytest.raises((aionap.exceptions.HttpClientError, aionap.exceptions.HttpNotFoundError)):
                await resource.get()
        elif 500 <= code <= 599:
            with pytest.raises(aionap.exceptions.HttpServerError):
                await resource.get()
        else:
            await resource.get()
        assert resource._.status == code


@pytest.mark.parametrize("format", [f for f in aionap.serialize.SERIALIZERS])
async def test_post_data(httpbin, format):
    data = {'foo': 'bar'}
    serializer = aionap.serialize.Serializer().get_serializer(name=format)
    api = aionap.API(httpbin.url, format=format)
    async with api.post as resource:
        resp = await resource.post(data=data)
        assert format in resp['headers'].get('Accept')
        assert format in resp['headers'].get('Content-Type')
        assert serializer.dumps(data) == resp['data']


async def test_send_files(httpbin):
    """POST and PUT files."""
    assert "TODO" == "DONE"
