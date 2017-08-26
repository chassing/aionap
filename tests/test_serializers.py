
import json
import pytest
import yaml

from aionap.serialize import JsonSerializer
from aionap.serialize import Serializer
from aionap.serialize import YamlSerializer


@pytest.fixture
def data():
    return {
        "foo": "bar",
    }


@pytest.fixture
def data_as(data):
    def dumps(format):
        if format == 'json':
            return json.dumps(data)
        if format == 'yaml':
            return yaml.dump(data)
        raise Exception('Unknown format')
    return dumps


@pytest.mark.parametrize("format, content_type, klass", [
    ('json', 'application/json', JsonSerializer),
    ('json', 'application/x-javascript', JsonSerializer),
    ('json', 'text/javascript', JsonSerializer),
    ('json', 'text/x-javascript', JsonSerializer),
    ('json', 'text/x-json', JsonSerializer),
    ('yaml', 'text/yaml', YamlSerializer),
    ('yaml', 'text/x-yaml', YamlSerializer),
    ('yaml', 'application/yaml', YamlSerializer),
    ('yaml', 'application/x-yaml', YamlSerializer),
])
def test_serializers(data, data_as, format, content_type, klass):
    format_serializer = Serializer().get_serializer(content_type=content_type)
    assert isinstance(format_serializer, klass)
    result = format_serializer.dumps(data)
    assert result == data_as(format)
    assert data == format_serializer.loads(result)
