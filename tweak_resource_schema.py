#!/usr/bin/env python

import tools


import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


this = None


def add_Custom(resource_schema):
    # add Custom::* resource
    try:
        resource_schema['definitions']['resource_types']['AWS::CloudFormation::CustomResource']['properties']['Type'] = {
            "oneOf": [
                {
                    "enum": [
                        "AWS::CloudFormation::CustomResource"
                    ]
                },
                {
                    "pattern": "^Custom::.*"
                }
            ]
        }
    except KeyError:
        pass


def fix_RecordSetGroup(resource_schema):
    try:
        (resource_schema['definitions']['resource_types']
        ['AWS::Route53::RecordSetGroup']['properties']['Properties']
        ['properties'])['RecordSets'] = {
            "type": "array",
            "items": {
                "$ref": "#/definitions/resource_types/AWS::Route53::RecordSet/properties/Properties"
            }
        }
    except KeyError:
        pass


def add_CreationPolicy(resource_schema):
    pq = tools.get_pq(tools.BASE + 'aws-attribute-creationpolicy.html')
    para = pq('#main-col-body p').filter(
        lambda p: 'resources that support creation policies' in pq(this).text()
    )
    types = [pq(a).text() for a in para('a')]
    for t in types:
        try:
            (resource_schema['definitions']['resource_types'][t]['properties']
             )['CreationPolicy'] = {
                "$ref": "#/definitions/attributes/CreationPolicy"
            }
        except KeyError:
            pass


def add_UpdatePolicy(resource_schema):
    try:
        (
            resource_schema['definitions']['resource_types']
            ['AWS::AutoScaling::AutoScalingGroup']['properties']
        )['UpdatePolicy'] = {
            "$ref": "#/definitions/attributes/UpdatePolicy"
        }
    except KeyError:
        pass


def main(argv):
    sess = CacheControl(requests.Session(),
                        cache=FileCache('.web_cache'))
    requests.get = sess.get
    resource_schema = tools.load(sys.argv[1])

    fix_RecordSetGroup(resource_schema)
    add_Custom(resource_schema)
    add_CreationPolicy(resource_schema)
    add_UpdatePolicy(resource_schema)

    if len(argv) == 3 and argv[2].endswith('json'):
        tools.write(resource_schema, argv[1])
    else:
        print tools.print_(resource_schema)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
