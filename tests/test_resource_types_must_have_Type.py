import jsonschema
import json
import pytest

valid = {
    "Type": "AWS::IAM::User",
    "Properties": {
        "Path": "/"
    }
}

invalid = {
    "Properties": {
        "Path": "/"
    }
}

resource_schema = json.load(open('resource.json'))


def test_valid():
    jsonschema.validate(valid, resource_schema)


def test_invalid():
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid, resource_schema)
