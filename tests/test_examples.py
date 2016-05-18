import json
import pytest
import glob
import val


schema = json.load(open('schema.json'))


@pytest.mark.parametrize("template", glob.glob('tests/examples/*.template'))
def test_template(template):
    if 'OpenStack' in template:
        pytest.skip('OpenStack is not supported')
    instance = json.load(open(template))
    val.val(instance, schema)
