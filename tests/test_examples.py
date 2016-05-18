import jsonschema
import json
import pytest
import glob
import os


schema_str = open('schema.json').read()
schema_str = schema_str.replace(
    '/home/ilya/jsonschema/cloudformation-jsonschema',
    os.getcwd()
)
schema = json.loads(schema_str)


def validate_resource(resource, schema):
    resource_types = schema['definitions']['resource_types']
    resource_type = resource['Type']
    if resource_type not in resource_types.keys():
        raise ValueError('Resource type "{}" unknown'.format(resource_type))
    resource_schema = resource_types[resource_type].copy()
    resource_schema['definitions'] = schema['definitions']
    jsonschema.validate(resource, resource_schema)


@pytest.mark.parametrize("template", glob.glob('tests/examples/*.template'))
def test_fn_base64_valid(template):
    instance = json.load(open(template))
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError as e:
        if '/'.join(e.absolute_schema_path) == 'properties/Resources/patternProperties/^[a-zA-Z0-9]+$/oneOf':
            validate_resource(e.instance, e.schema)
        else:
            raise
