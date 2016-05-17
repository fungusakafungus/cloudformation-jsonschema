import jsonschema
import json
import pytest


resource_schema = json.load(open('resource-stage1.json'))


def merge(a, b, path=None):
    """merges b into a
    http://stackoverflow.com/a/7205107/291124
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


@pytest.mark.parametrize("instance", [
    {
        "Type": "sometype",
        "test": {
            "Fn::Base64": "string value"
        }
    },
    {
        "Type": "sometype",
        "test": {
            "Fn::Base64": {"Ref": "resource"}
        }
    },
    {
        "Type": "sometype",
        "test": {
            "Fn::Base64": {"Fn::Base64": "doubleencode"}
        }
    },
])
def test_fn_base64_valid(instance):
    amended_schema = {
        "properties": {
            "test": {
                "$ref": "#/definitions/basic_types/functions/Fn::Base64"
            }
        }
    }
    merge(amended_schema, resource_schema)
    jsonschema.validate(instance, amended_schema)


@pytest.mark.parametrize("instance", [
    {
        "Type": "sometype",
        "test": {
            "Fn::Base64": True
        }
    },
    {
        "Type": "sometype",
        "test": {
            "Fn::Base64": {"invalidfunction": "arg"}
        }
    },
    {
        "Type": "sometype",
        "test": {
            "Fn::Base64": "arg",
            "extraProp": 1
        }
    },
])
def test_fn_base64_invalid(instance):
    amended_schema = {
        "properties": {
            "test": {
                "$ref": "#/definitions/basic_types/functions/Fn::Base64"
            }
        }
    }
    merge(amended_schema, resource_schema)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance, amended_schema)


@pytest.mark.parametrize("instance", [
    {
        "Type": "sometype",
        "test": {
            "Fn::FindInMap": ["MapName", "TopLevelKey", "SecondLevelKey"]
        }
    },
    {
        "Type": "sometype",
        "test": {
            "Fn::FindInMap": [{"Ref": "MapName"}, "TopLevelKey", "SecondLevelKey"]
        }
    },
    {
        "Type": "sometype",
        "test": {
            "Fn::FindInMap": ["MapName", {"Ref": "AWS::Region"}, "SecondLevelKey"]
        }
    },
    {
        "Type": "sometype",
        "test": {
            "Fn::FindInMap": [
                {"Fn::FindInMap": ["AnotherMapName", "TopLevelKey", "SecondLevelKey"]},
                "TopLevelKey",
                "SecondLevelKey"
            ]
        }
    },
])
def test_fn_findinmap_valid(instance):
    amended_schema = {
        "properties": {
            "test": {
                "$ref": "#/definitions/basic_types/functions/Fn::FindInMap"
            }
        }
    }
    merge(amended_schema, resource_schema)
    jsonschema.validate(instance, amended_schema)
