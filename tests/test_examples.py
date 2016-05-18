import jsonschema
import json
import pytest
import glob
import os


schema_str = open('schema.json').read()
schema_str.replace(
    '/home/ilya/jsonschema/cloudformation-jsonschema/',
    os.getcwd()
)
schema = json.loads(schema_str)


@pytest.mark.parametrize("template", glob.glob('tests/examples/*.template'))
def test_fn_base64_valid(template):
    instance = json.load(open(template))
    jsonschema.validate(instance, schema)
