import jsonschema
import os.path

import tools


def resolve_and_validate(instance, schema):
    resolver = jsonschema.RefResolver(
        'file:' + os.path.abspath(os.path.dirname(__file__)) + '/',
        schema
    )
    jsonschema.validate(instance, schema,
                        cls=jsonschema.Draft4Validator, resolver=resolver)


def validate_resource(resource, schema):
    resource_types = schema['definitions']['resource_types']
    resource_type = resource['Type']
    if resource_type.startswith('Custom::'):
        resource_type = 'AWS::CloudFormation::CustomResource'
    if resource_type not in resource_types.keys():
        raise ValueError('Resource type "{}" unknown'.format(resource_type))
    resource_schema = resource_types[resource_type].copy()
    resource_schema['definitions'] = schema['definitions']
    resolve_and_validate(resource, resource_schema)


def val(instance, schema, definition=None):
    if definition:
        schema = {
            "$ref": definition,
            "definitions": schema['definitions'],
        }
    try:
        resolve_and_validate(instance, schema)
    except jsonschema.ValidationError as e:
        schema_path = '/'.join(str(p) for p in e.absolute_schema_path)
        if schema_path in ['properties/Resources/patternProperties/^[a-zA-Z0-9]+$/oneOf',
                           'properties/Resources/patternProperties/^[a-zA-Z0-9]+$/additionalProperties']:
            validate_resource(tools.OD(e.instance), tools.OD(e.schema))
        raise


def validate_and_return_error(instance, schema):
    try:
        val(instance, schema)
    except jsonschema.ValidationError as e:
        return e
