
import posixpath

from urllib.parse import urlsplit
from urllib.parse import urlunsplit


def urljoin(base, *args):
    """Helper function to join an arbitrary number of url segments together."""
    scheme, netloc, path, query, fragment = urlsplit(base)
    path = path if len(path) else "/"
    path = posixpath.join(path, *[('%s' % x) for x in args])
    return urlunsplit([scheme, netloc, path, query, fragment])


def transform_url_parameters(params):
    """Transform python dictionary to aiohttp valid url parameters.

    support for:
    key=["a", "b"] -> ?key=a&key=b
    """
    if isinstance(params, list):
        # nothing to do
        return params

    p = []
    for key, value in params.items():
        if isinstance(value, list) or isinstance(value, tuple):
            p += [(key, v) for v in value]
        else:
            p.append((key, value))
    return p
