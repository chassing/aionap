
import pytest

import aionap.utils


@pytest.mark.parametrize("urljoin_args, expected", [
    # http + base with trailing slash
    (["http://example.com/"], "http://example.com/"),
    (["http://example.com/", "test"], "http://example.com/test"),
    (["http://example.com/", "test", "example"], "http://example.com/test/example"),
    # http + base without trailing slash
    (["http://example.com"], "http://example.com/"),
    (["http://example.com", "test"], "http://example.com/test"),
    (["http://example.com", "test", "example"], "http://example.com/test/example"),
    # https + base with trailing slash
    (["https://example.com/"], "https://example.com/"),
    (["https://example.com/", "test"], "https://example.com/test"),
    (["https://example.com/", "test", "example"], "https://example.com/test/example"),
    # https + base without trailing slash
    (["https://example.com"], "https://example.com/"),
    (["https://example.com", "test"], "https://example.com/test"),
    (["https://example.com", "test", "example"], "https://example.com/test/example"),
    # http + port + base with trailing slash
    (["http://example.com:80/"], "http://example.com:80/"),
    (["http://example.com:80/", "test"], "http://example.com:80/test"),
    (["http://example.com:80/", "test", "example"], "http://example.com:80/test/example"),
    # http + port +base without trailing slash
    (["http://example.com:80"], "http://example.com:80/"),
    (["http://example.com:80", "test"], "http://example.com:80/test"),
    (["http://example.com:80", "test", "example"], "http://example.com:80/test/example"),
    # https + port + base with trailing slash
    (["https://example.com:443/"], "https://example.com:443/"),
    (["https://example.com:443/", "test"], "https://example.com:443/test"),
    (["https://example.com:443/", "test", "example"], "https://example.com:443/test/example"),
    # https + port + base without trailing slash
    (["https://example.com:443"], "https://example.com:443/"),
    (["https://example.com:443", "test"], "https://example.com:443/test"),
    (["https://example.com:443", "test", "example"], "https://example.com:443/test/example"),
    # path
    (["/"], "/"),
    (["/", "test"], "/test"),
    (["/", "test", "example"], "/test/example"),
    # with base path
    (["/path/"], "/path/"),
    (["/path/", "test"], "/path/test"),
    (["/path/", "test", "example"], "/path/test/example"),
    # trailing slash
    (["http://example.com/", "test/"], "http://example.com/test/"),
    (["http://example.com/", "test/", "example/"], "http://example.com/test/example/"),
])
def test_urljoin(urljoin_args, expected):
    assert aionap.utils.urljoin(*urljoin_args) == expected


@pytest.mark.parametrize("params, expected", [
    # empty
    ({}, []),
    ([], []),
    # no lists
    ({'key1': 'value1'}, [('key1', 'value1')]),
    ({'key1': 'value1', 'key2': 'value2'}, [('key1', 'value1'), ('key2', 'value2')]),
    # just lists
    ({'key1': ['value1']}, [('key1', 'value1')]),
    ({'key1': ['value1', 'value2']}, [('key1', 'value1'), ('key1', 'value2')]),
    ({'key1': ['value1'], 'key2': ['value2']}, [('key1', 'value1'), ('key2', 'value2')]),
    ({'key1': ['value1', 'value2'], 'key2': ['value1', 'value2']}, [('key1', 'value1'), ('key1', 'value2'), ('key2', 'value1'), ('key2', 'value2')]),
    # mixed
    ({'key1': ['value1'], 'd': 'v'}, [('key1', 'value1'), ('d', 'v')]),
    ({'key1': ['value1', 'value2'], 'd': 'v'}, [('key1', 'value1'), ('key1', 'value2'), ('d', 'v')]),
    ({'key1': ['value1'], 'key2': ['value2'], 'd': 'v'}, [('key1', 'value1'), ('key2', 'value2'), ('d', 'v')]),
    ({'key1': ['value1', 'value2'], 'key2': ['value1', 'value2'], 'd': 'v'}, [('key1', 'value1'), ('key1', 'value2'), ('key2', 'value1'), ('key2', 'value2'), ('d', 'v')]),
])
def test_transform_url_parameters(params, expected):
    assert sorted(aionap.utils.transform_url_parameters(params)) == sorted(expected)
