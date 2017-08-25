
class AioNapBaseException(Exception):
    """All AioNap exceptions inherit from this exception."""


class AioNapHttpBaseException(AioNapBaseException):
    """All Slumber HTTP Exceptions inherit from this exception."""

    def __init__(self, *args, **kwargs):
        """Init."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__(*args)


class HttpClientError(AioNapHttpBaseException):
    """Called when the server tells us there was a client error (4xx)."""


class HttpNotFoundError(HttpClientError):
    """Called when the server sends a 404 error."""


class HttpServerError(AioNapHttpBaseException):
    """Called when the server tells us there was a server error (5xx)."""


class SerializerNoAvailable(AioNapBaseException):
    """There are no available Serializers."""


class SerializerNotAvailable(AioNapBaseException):
    """The chosen Serializer is not available."""


class ImproperlyConfigured(AioNapBaseException):
    """AioNap is somehow improperly configured."""
