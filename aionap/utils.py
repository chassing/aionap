
import posixpath

from urllib.parse import urlsplit
from urllib.parse import urlunsplit


def urljoin(base, *args):
    """Helper function to join an arbitrary number of url segments together."""
    scheme, netloc, path, query, fragment = urlsplit(base)
    path = path if len(path) else "/"
    path = posixpath.join(path, *[('%s' % x) for x in args])
    return urlunsplit([scheme, netloc, path, query, fragment])
