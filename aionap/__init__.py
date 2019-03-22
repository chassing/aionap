
import aiohttp

from . import exceptions
from .serialize import Serializer
from .utils import transform_url_parameters, urljoin


__all__ = ["Resource", "API"]


class AttributesMixin:
    """A Mixin that allows access to an undefined attribute on a class."""

    def __getattr__(self, item):
        # Don't allow access to 'private' by convention attributes.
        # @@@: How would this work with resources names that begin with
        # underscores?
        if item.startswith("_"):
            raise AttributeError(item)

        kwargs = dict(self._store)
        kwargs.update({"base_url": urljoin(self._store["base_url"], item)})

        return self._get_resource(**kwargs)


class Resource(AttributesMixin):
    """Resource provides the main functionality behind aionap.

    It handles the attribute -> url, kwarg -> query param, and other related behind the scenes
    python to HTTP transformations. It's goal is to represent a single resource
    which may or may not have children.
    """

    def __init__(self, *args, **kwargs):
        """Init."""
        self._store = kwargs

    def __call__(self, id=None, format=None, url_override=None):
        """Return a new instance of self modified by one or more of the available parameters.

        These allows us to do things like override format for a specific request, and enables
        the api.resource(ID).get() syntax to get a specific resource by it's ID.
        """
        # Short Circuit out if the call is empty
        if id is None and format is None and url_override is None:
            return self

        kwargs = dict(self._store)

        if id is not None:
            kwargs["base_url"] = urljoin(self._store["base_url"], id)

        if format is not None:
            kwargs["format"] = format

        if url_override is not None:
            # @@@ This is hacky and we should probably figure out a better way
            #    of handling the case when a POST/PUT doesn't return an object
            #    but a Location to an object that we need to GET.
            kwargs["base_url"] = url_override

        kwargs["session"] = self._store["session"]

        return self._get_resource(**kwargs)

    async def _request(self, method, data=None, file=None, headers=None, params=None):
        serializer = self._store["serializer"]
        url = self.url

        _headers = {"accept": serializer.get_content_type()}

        if not file:
            if data is not None:
                _headers["content-type"] = serializer.get_content_type()
                data = serializer.dumps(data)
        else:
            if data is None:
                data = {}
            data['file'] = file

        if headers:
            _headers.update(headers)

        resp = await self._store["session"].request(method, url, data=data, params=params, headers=_headers)
        self._ = resp

        if 400 <= resp.status <= 499:
            exception_class = exceptions.HttpNotFoundError if resp.status == 404 else exceptions.HttpClientError
            raise exception_class("Client Error %s: %s" % (resp.status, url), response=resp, content=await self._try_to_serialize_response(resp))
        elif 500 <= resp.status <= 599:
            raise exceptions.HttpServerError("Server Error %s: %s" % (resp.status, url), response=resp, content=await self._try_to_serialize_response(resp))

        return resp

    async def _try_to_serialize_response(self, resp):
        s = self._store["serializer"]
        if resp.status in [204, 205]:
            return

        content = await resp.read()
        if resp.headers.get("content-type", None) and content:
            content_type = resp.headers.get("content-type").split(";")[0].strip()

            try:
                # get serializer
                stype = s.get_serializer(content_type=content_type)
            except exceptions.SerializerNotAvailable:
                return content
            # serialize content
            return stype.loads(content)
        return content

    async def _process_response(self, resp):
        if 200 <= resp.status <= 299:
            decoded = await self._try_to_serialize_response(resp)
        else:
            # @@@ We should probably do some sort of error here? (Is this even possible?)
            decoded = None

        if self._store["raw"]:
            return (resp, decoded)

        return decoded

    async def _do_verb_request(self, verb, data=None, file=None, headers=None, params=None):
        resp = await self._request(verb, data=data, file=file, headers=headers, params=transform_url_parameters(params))
        return await self._process_response(resp)

    def as_raw(self):
        """."""
        self._store["raw"] = True
        return self

    async def get(self, headers=None, **kwargs):
        """GET request."""
        return await self._do_verb_request("GET", headers=headers, params=kwargs)

    async def post(self, data=None, file=None, headers=None, **kwargs):
        """POST.

        file: file-like object
        """
        return await self._do_verb_request("POST", data=data, file=file, headers=headers, params=kwargs)

    async def patch(self, data=None, file=None, headers=None, **kwargs):
        """PATCH."""
        return await self._do_verb_request("PATCH", data=data, file=file, headers=headers, params=kwargs)

    async def put(self, data=None, file=None, headers=None, **kwargs):
        """PUT."""
        return await self._do_verb_request("PUT", data=data, file=file, headers=headers, params=kwargs)

    async def delete(self, headers=None, **kwargs):
        """DELETE."""
        return await self._do_verb_request("DELETE", headers=headers, params=kwargs)

    # async def options(self, **kwargs):
    #     return await self._do_verb_request("OPTIONS", params=kwargs)

    # async def head(self, **kwargs):
    #     return await self._do_verb_request("HEAD", params=kwargs)

    @property
    def url(self):
        """Return url."""
        url = self._store["base_url"]

        if self._store["append_slash"] and not url.endswith("/"):
            url += "/"

        return url

    def _get_resource(self, **kwargs):
        return self.__class__(**kwargs)


class API(AttributesMixin):
    """Main class."""

    resource_class = Resource

    def __init__(self, base_url=None, auth=None, format=None, append_slash=False, session=None, serializer=None, raw=False, session_kwargs=None):
        """Init."""
        if serializer is None:
            serializer = Serializer(default=format)

        if not session_kwargs:
            session_kwargs = {}

        if auth is not None:
            session_kwargs['auth'] = aiohttp.BasicAuth(*auth)

        if session is None:
            session = aiohttp.ClientSession(**session_kwargs)

        # internal config
        self._store = {
            "base_url": base_url,
            "format": format if format is not None else "json",
            "append_slash": append_slash,
            "session": session,
            "serializer": serializer,
            "raw": raw,
        }

        # Do some Checks for Required Values
        if self._store.get("base_url") is None:
            raise exceptions.ImproperlyConfigured("base_url is required")

    async def __aenter__(self):
        """Asyncio with enter."""
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Asyncio with exit."""
        await self.close()

    async def close(self):
        """Close underlying session."""
        await self._store['session'].close()

    def _get_resource(self, **kwargs):
        return self.resource_class(**kwargs)
