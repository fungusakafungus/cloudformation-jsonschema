import jsonschema
import json
import pytest
import val


basic_types_schema = json.load(open('basic_types.json'))


@pytest.mark.parametrize("instance", [
    {
        "Fn::Base64": "string value"
    },
    {
        "Fn::Base64": {"Ref": "resource"}
    },
    {
        "Fn::Base64": {"Fn::Base64": "doubleencode"}
    },
])
def test_fn_base64_valid(instance):
    val.val(instance, basic_types_schema,
            definition="#/definitions/functions/Fn::Base64")


@pytest.mark.parametrize("instance", [
    {
        "Fn::Base64": True
    },
    {
        "Fn::Base64": {"invalidfunction": "arg"}
    },
    {
        "Fn::Base64": "arg",
        "extraProp": 1
    },
])
def test_fn_base64_invalid(instance):
    with pytest.raises(jsonschema.ValidationError):
        val.val(instance, basic_types_schema,
                definition="#/definitions/functions/Fn::Base64")


@pytest.mark.parametrize("instance", [
    {
        "Fn::FindInMap": ["MapName", "TopLevelKey", "SecondLevelKey"]
    },
    {
        "Fn::FindInMap": [{"Ref": "MapName"}, "TopLevelKey", "SecondLevelKey"]
    },
    {
        "Fn::FindInMap": ["MapName", {"Ref": "AWS::Region"}, "SecondLevelKey"]
    },
    {
        "Fn::FindInMap": [
            {"Fn::FindInMap": ["AnotherMapName", "TopLevelKey", "SecondLevelKey"]},
            "TopLevelKey",
            "SecondLevelKey"
        ]
    },
])
def test_fn_findinmap_valid(instance):
    val.val(instance, basic_types_schema,
            definition="#/definitions/functions/Fn::FindInMap")


@pytest.mark.parametrize("instance", [
    {'Fn::If': ['IsMultiNodeCluster', {'Ref': 'NumberOfNodes'}, {'Ref': 'AWS::NoValue'}]},
    {'Fn::If': ['Cond1', 1, 2]},
])
def test_fn_if_valid(instance):
    val.val(instance, basic_types_schema,
            definition="#/definitions/condition_functions/Fn::If")


@pytest.mark.parametrize("instance", [
    {'Fn::If': [['not a string'], 1, 2]},
    {'Fn::If': ['one', 'too', 'many', 'args']},
    {'Fn::If': [{"Ref": "not a ref"}, 1, 2]},
])
def test_fn_if_invalid(instance):
    with pytest.raises(jsonschema.ValidationError):
        val.val(instance, basic_types_schema,
                definition="#/definitions/condition_functions/Fn::If")


@pytest.mark.parametrize("instance", [
    {'Fn::GetAZs': ''},
    {'Fn::GetAZs': 'us-east-1'},
    {"Fn::GetAZs": {"Ref": "AWS::Region"}},
])
def test_fn_getazs_valid(instance):
    val.val(instance, basic_types_schema,
            definition="#/definitions/functions/Fn::GetAZs")


@pytest.mark.parametrize("instance", [
    {'Fn::GetAZs': []},
    {'Fn::GetAZs': {'Fn::Join': ['-', ['us', 'east', '1']]}},
    {"Fn::GetAZs": {"Ref": "AWS::Region", 'extra': 3}},
])
def test_fn_getazs_invalid(instance):
    with pytest.raises(jsonschema.ValidationError):
        val.val(instance, basic_types_schema,
                definition="#/definitions/functions/Fn::GetAZs")


@pytest.mark.parametrize("instance", [
    {'Fn::GetAZs': 'is a function'},
    ['string', 'string'],
    ['string', {'Ref': 'res'}],
    {'Fn::If': [
        'Is-EC2-VPC',
        [{'Fn::GetAtt': ['DBEC2SecurityGroup', 'GroupId']}],
        {'Ref': 'AWS::NoValue'}
    ]},
])
def test_string_list_valid(instance):
    val.val(instance, basic_types_schema,
            definition="#/definitions/list<string>")

long_if = {'Fn::If': [
    'Is-EC2-VPC',
    [{'Fn::GetAtt': ['DBEC2SecurityGroup', 'GroupId']}],
    {'Ref': 'AWS::NoValue'}
]}


@pytest.mark.parametrize(("instance", "definition"), [
    (long_if, "#/definitions/string"),
    (long_if, "#/definitions/function"),
    (long_if, "#/definitions/condition_function"),
    (long_if, "#/definitions/condition_functions/Fn::If"),
])
def test_string_function_valid(instance, definition):
    val.val(instance, basic_types_schema,
            definition=definition)
