# coding: utf-8
from pyquery import PyQuery as q
import json
from collections import OrderedDict
from copy import deepcopy

this = None
BASE = 'http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/'


class OD(OrderedDict):
    def __repr__(self):
        return print_(self)


def load(filename='resource.json'):
    schema = json.load(open(filename), object_pairs_hook=OD)
    return schema


def get_pq(uri=BASE + 'aws-template-resource-type-ref.html'):
    h = q(uri, headers={
        'user-agent':
        'https://github.com/fungusakafungus/cloudformation-jsonschema'
    })
    h.make_links_absolute()
    return h


def all_resource_properties_hrefs():
    h = get_pq(BASE + 'aws-product-property-reference.html')
    res = OD(
        (a1.attr('href'), a1.text())
        for a1 in [q(a)
                   for a
                   in h('#main-col-body li a')
                   ]
    )
    return res


def all_resource_hrefs():
    h = get_pq(BASE + 'aws-template-resource-type-ref.html')
    all_resource_hrefs = OD(
        (a1.text().strip(), a1.attr('href'))
        for a1 in [q(a) for a in h('#main-col-body li a')])
    return all_resource_hrefs


def write(schema, filename='resource.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(schema, indent=4, separators=(',', ': ')))
        f.write("\n")


def print_(schema):
    return json.dumps(schema, indent=4)


def get_all_resource_type_names():
    h = get_pq(BASE + 'aws-template-resource-type-ref.html')
    result = [
        a.strip()
        for a
        in h('#main-col-body li a').map(lambda x: this.text)
    ]
    return result


def get_resource_types(schema):
    if 'definitions' not in schema:
        schema['definitions'] = OD()
    if 'resource_types' not in schema['definitions']:
        schema['definitions']['resource_types'] = OD()

    return schema['definitions']['resource_types']


def get_oneOf(resource_type_names):
    return [{"$ref": "#/definitions/resource_types/" + i} for i in resource_type_names]


def make_resource_type_definition(schema, resource_type_name):
    result = deepcopy(schema['definitions']['resource_template'])
    result['properties']['Type']['enum'] = [resource_type_name]

    return result


def update_all_resource_patterns_by_name(schema, resource_type_names):
    resource_types = get_resource_types(schema)
    for rt_name in resource_type_names:
        rt_definition = make_resource_type_definition(
            schema,
            rt_name
        )
        resource_types[rt_name] = rt_definition
    schema['oneOf'] = get_oneOf(resource_type_names)
    # put definitions last
    schema['definitions'] = schema.pop('definitions')
