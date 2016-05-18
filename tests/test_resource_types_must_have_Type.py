import val
import json
import jsonschema
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
    val.val(valid, resource_schema)


def test_invalid():
    with pytest.raises(jsonschema.ValidationError):
        val.val(invalid, resource_schema)
