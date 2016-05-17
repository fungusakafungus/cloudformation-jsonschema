valid = """
{
    "Type" : "AWS::IAM::User",
    "Properties" : {
        "Path" : "/"
    }
}
"""

invalid = """
{
    "Properties" : {
        "Path" : "/"
    }
}
"""

import jsonschema
import json
import pytest

resource_schema = json.load(open('resource.json'))
def test_valid():
    jsonschema.validate(json.loads(valid), resource_schema)

def test_invalid():
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(json.load(open('tests/no-type.json')), resource_schema)
    assert "'Type' is a required property" in excinfo.value.message
