import json
import pytest
import glob
import val


schema = json.load(open('schema.json'))


@pytest.mark.parametrize("template", glob.glob('tests/examples-*/*.template'))
def test_template(template):
    if 'troposphere/EMR_Cluster' in template:
        pytest.skip('troposphere/EMR_Cluster uses undocumented AWS::EMR::Cluster.EbsConfiguration')
    if 'OpenStack' in template:
        pytest.skip('OpenStack is not supported')
    instance = json.load(open(template))
    val.val(instance, schema)


import py.io
import py._io.saferepr


def saferepr(obj, maxsize=2400):
    """ return a size-limited safe repr-string for the given object.
    Failing __repr__ functions of user instances will be represented
    with a short exception info and 'saferepr' generally takes
    care to never raise exceptions itself.  This function is a wrapper
    around the Repr/reprlib functionality of the standard 2.6 lib.
    """
    # review exception handling
    srepr = py._io.saferepr.SafeRepr()
    srepr.maxstring = maxsize
    srepr.maxsize = maxsize
    srepr.maxother = 1600
    return srepr.repr(obj)


py.io.saferepr = saferepr
