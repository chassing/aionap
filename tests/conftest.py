
import asyncio
import collections

import pytest


class Url(str):
    """String like object with '/' as extension."""

    def __div__(self, other):
        """Url / foobar support."""
        return f"{self}/{other}"

    __truediv__ = __div__

Server = collections.namedtuple('Server', ['url', 'host', 'port'])


@pytest.fixture
async def httpbin(unused_tcp_port):
    httpbin_cmd = f"python -m httpbin.core --port={unused_tcp_port}"
    # proc = await asyncio.create_subprocess_exec(*httpbin_cmd.split(), loop=event_loop)
    proc = await asyncio.create_subprocess_exec(*httpbin_cmd.split())
    host = "localhost"
    port = unused_tcp_port
    yield Server(Url(f"http://{host}:{port}"), host, port)
    proc.kill()
