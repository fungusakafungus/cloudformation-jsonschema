#!/usr/bin/env python

import tools
import resource_properties
import val

import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


def main(argv):
    sess = CacheControl(requests.Session(),
                        cache=FileCache('.web_cache'))
    requests.get = sess.get

    resource_schema = tools.load('resource-stage1.json')
    # resource has a type
    val.val({"Type": "Something"}, resource_schema)

    tools.update_all_resource_patterns_by_name(resource_schema)
    # all resource types are known
    val.val({"Type": "AWS::Lambda::Function"}, resource_schema)

    resource_type_names = tools.all_resource_patterns_by_name().keys()
    for resource_type_name in resource_type_names:
        print >> sys.stderr, resource_type_name
        resource_properties.set_resource_properties(resource_schema, resource_type_name)
    # simple resource properties are validated
    val.val(
        {
            "Type": "AWS::IAM::User",
            "Properties": {
                "Groups": ["some_group"]
            }
        },
        resource_schema
    )
    all_properties = resource_properties.all_res_properties()
    resource_schema['definitions']['property_types'] = all_properties

    # fix inconsistencies
    resource_schema['definitions']['resource_types']['AWS::Route53::RecordSetGroup']['properties']['Properties']['properties']['RecordSets'] = {
        "type": "array",
        "items": {
            "$ref": "#/definitions/resource_types/AWS::Route53::RecordSet/properties/Properties"
        }
    }

    if len(argv) == 2 and argv[1].endswith('json'):
        tools.write(resource_schema, argv[1])
    else:
        print tools.print_(resource_schema)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
