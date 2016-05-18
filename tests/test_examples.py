import jsonschema
import json
import pytest
import glob


schema = json.load(open('schema.json'))


@pytest.mark.parametrize("template", glob.glob('tests/examples/*.template'))
def test_fn_base64_valid(template):
    instance = json.load(open(template))
    jsonschema.validate(instance, schema)
