# coding: utf-8
from pyquery import PyQuery as q
import json
from collections import OrderedDict

this = None
BASE = 'http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/'


def load(filename='resource.json'):
    schema = json.load(open(filename), object_pairs_hook=OrderedDict)
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
    res = OrderedDict(
        (a1.attr('href'), a1.text())
        for a1 in [q(a)
                   for a
                   in h('#main-col-body li a')
                   ]
    )
    return res


def all_resource_hrefs():
    h = get_pq(BASE + 'aws-template-resource-type-ref.html')
    all_resource_hrefs = OrderedDict(
        (a1.text().strip(), a1.attr('href'))
        for a1 in [q(a) for a in h('#main-col-body li a')])
    return all_resource_hrefs


def write(schema, filename='resource.json'):
    with open(filename, 'w') as f:
        f.write(json.dumps(schema, indent=4, separators=(',', ': ')))


def print_(schema):
    return json.dumps(schema, indent=4)


def all_resource_patterns_by_name():
    h = get_pq(BASE + 'aws-template-resource-type-ref.html')
    all_resource_patterns_by_name = OrderedDict(
        (
            a.strip(),
            {'properties': {'Type': {'enum': [a.strip()]}}}
        )
        for a in h('#main-col-body li a').map(lambda x: this.text)
    )
    return all_resource_patterns_by_name


def resources_dict(schema):
    if 'definitions' not in schema:
        schema['definitions'] = OrderedDict(
            {'resource_types': OrderedDict()}
        )

    return schema['definitions']['resource_types']


def get_oneOf():
    res_names = all_resource_patterns_by_name().keys()
    return [{"$ref": "#/definitions/resource_types/" + i} for i in res_names]


def update_all_resource_patterns_by_name(schema):
    o = resources_dict(schema)
    new = all_resource_patterns_by_name()
    new.update(o)
    schema['oneOf'] = get_oneOf()
    schema['definitions']['resource_types'] = new
    # put definitions last
    schema['definitions'] = schema.pop('definitions')
