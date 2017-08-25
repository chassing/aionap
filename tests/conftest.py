
import collections
import contextlib
import pytest
import socket
import subprocess
import time

from urllib.error import URLError
from urllib.request import urlopen


class Url(str):
    """String like object with '/' as extension."""

    def __div__(self, other):
        """Url / foobar support."""
        return f"{self}/{other}"

    __truediv__ = __div__

Server = collections.namedtuple('Server', ['url', 'host', 'port'])


def wait_for_httpbin(url):
    retry = 0
    timeout = 0.1
    # try to reach httpbin in max 5s
    while retry < 50:
        try:
            with urlopen(url) as resp:
                assert resp.getcode() == 200
                return
        except URLError:
            time.sleep(timeout)
            retry += 1

    raise Exception("httpbin server not reachable!!!")


@pytest.fixture(scope='session')
def tcp_port():
    """Find an unused localhost TCP port from 1024-65535 and return it."""
    with contextlib.closing(socket.socket()) as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


@pytest.yield_fixture(scope='session')
def httpbin(tcp_port):
    httpbin_cmd = f"python -m httpbin.core --port={tcp_port}"
    httpbin_proc = subprocess.Popen(httpbin_cmd.split(" "))
    host = "localhost"
    port = tcp_port
    url = Url(f"http://{host}:{port}")
    # wait until httpbin as been started
    wait_for_httpbin(url)
    # return and run tests
    yield Server(url, host, port)
    # kill httpbin
    httpbin_proc.kill()
