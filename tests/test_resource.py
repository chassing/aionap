
import aionap
import pytest

pytestmark = pytest.mark.asyncio


@pytest.fixture(params=[f for f in aionap.serialize.SERIALIZERS])
def format(request):
    return request.param


@pytest.fixture(params=['get', 'post', 'put', 'patch', 'delete'])
def http_method(request):
    return request.param


@pytest.fixture(params=['post', 'put', 'patch'])
def http_send_method(request):
    return request.param


async def test_plain_methods(httpbin, http_method):
    """Just the plain http methods without data, params etc."""
    async with aionap.API(httpbin.url, append_slash=False) as api:
        resource = api.anything
        # resource.get()
        resp = await getattr(resource, http_method)()
        assert resp['method'] == http_method.upper()


async def test_params(httpbin, http_method):
    """Just the plain http methods without data, params etc."""
    async with aionap.API(httpbin.url, append_slash=False) as api:
        params = {'key': 'value', 'key2': 'value2'}
        resource = api.anything
        resp = await getattr(resource, http_method)(**params)
        assert resp['args'] == params


async def test_deep_nested_resource_urls(httpbin):
    """Test _get_resource and __call__."""
    async with aionap.API(httpbin.url) as api:
        resource = api.anything.deep.nested.resource.urls
        resp = await resource.get()
        assert resp['method'] == 'GET'
        assert resp['url'].endswith('deep/nested/resource/urls')


async def test_deep_nested_resource_urls_with_ids(httpbin):
    """Test _get_resource and __call__."""
    async with aionap.API(httpbin.url) as api:
        resource = api.anything.deep(1).nested(1).resource(1).urls(1)
        resp = await resource.get()
        assert resp['url'].endswith('/deep/1/nested/1/resource/1/urls/1')


async def test_deep_nested_resource_urls_with_name(httpbin):
    """Test _get_resource and __call__."""
    async with aionap.API(httpbin.url) as api:
        resource = api.anything.deep("name").nested("name").resource("name").urls("name")
        resp = await resource.get()
        assert resp['url'].endswith('/deep/name/nested/name/resource/name/urls/name')


async def test_close(httpbin):
    api = aionap.API(httpbin.url)
    await api.close()
    # should raise closed exception
    with pytest.raises(RuntimeError):
        await api.anything.resource.get()


async def test_append_slash(httpbin):
    async with aionap.API(httpbin.url, append_slash=True) as api:
        resource = api.anything.whatever
        resp = await resource.get()
    assert resp['url'].endswith('/')


async def test_no_append_slash(httpbin):
    async with aionap.API(httpbin.url, append_slash=False) as api:
        resource = api.anything.whatever
        resp = await resource.get()
        assert not resp['url'].endswith('/')

async def test_default_no_append_slash(httpbin):
    async with aionap.API(httpbin.url) as api:
        resource = api.anything.whatever
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
    async with aionap.API(httpbin.url) as api:
        resource = api.status(code)
        if 300 <= code <= 399:
            resp = await resource.get()
            if code not in [300, 304]:
                # it's real location: XXX response, therefor test redirection
                code = 200
                # httpbin std redirect is to /get
                assert resp['url'].endswith('/get')
        elif 400 <= code <= 499:
            with pytest.raises((aionap.exceptions.HttpClientError, aionap.exceptions.HttpNotFoundError)) as excinfo:
                await resource.get()
            if code == 402:
                assert len(excinfo.value.content) > 0
            else:
                assert excinfo.value.content == b''
        elif 500 <= code <= 599:
            with pytest.raises(aionap.exceptions.HttpServerError) as excinfo:
                await resource.get()
            assert excinfo.value.content == b''
        else:
            await resource.get()
        assert resource._.status == code


async def test_send_data(httpbin, format, http_send_method):
    data = {'foo': 'bar'}
    serializer = aionap.serialize.Serializer().get_serializer(name=format)
    async with aionap.API(httpbin.url, format=format) as api:
        resource = getattr(api, http_send_method)
        resp = await getattr(resource, http_send_method)(data=data)
        assert format in resp['headers'].get('Accept')
        assert format in resp['headers'].get('Content-Type')
        assert serializer.dumps(data) == resp['data']


async def test_send_files(httpbin, tmpdir, http_send_method):
    """POST and PUT files."""
    TEST_STR = "TEST TEST TEST"
    tmpfile = tmpdir.join("tmp.txt")
    tmpfile.write(TEST_STR)
    async with aionap.API(httpbin.url) as api:
        resource = getattr(api, http_send_method)
        resp = await getattr(resource, http_send_method)(file=open(tmpfile, 'rb'))
        assert TEST_STR == resp['files']['file']


async def test_headers(httpbin, http_method):
    async with aionap.API(httpbin.url) as api:
        resource = getattr(api, http_method)
        resp = await getattr(resource, http_method)(headers={'X-Answer': '42'})
        assert resp['headers']['X-Answer'] == '42'


async def test_custom_content_type(httpbin, http_method):
    async with aionap.API(httpbin.url) as api:
        resource = getattr(api, http_method)
        resp = await getattr(resource, http_method)(headers={'content-type': 'application/foobar'})
        assert resp['headers']['Content-Type'] == 'application/foobar'

