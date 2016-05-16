#!/usr/bin/env python

import tools
import jsonschema
import resource_properties

import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


def main(argv):
    sess = CacheControl(requests.Session(),
                        cache=FileCache('.web_cache'))
    requests.get = sess.get

    schema = tools.load('resource-stage1.json')
    # resource has a type
    jsonschema.validate({"Type": "Something"}, schema)

    tools.update_all_resource_patterns_by_name(schema)
    # all resource types are known
    jsonschema.validate({"Type": "AWS::Lambda::Function"}, schema)

    resource_type_names = tools.all_resource_patterns_by_name().keys()
    for resource_type_name in resource_type_names:
        print >> sys.stderr, resource_type_name
        resource_properties.set_resource_properties(schema, resource_type_name)
    # simple resource properties are validated
    jsonschema.validate(
        {
            "Type": "AWS::IAM::User",
            "Properties": {
                "Groups": ["some_group"]
            }
        },
        schema
    )
    all_properties = resource_properties.all_res_properties()
    schema['definitions']['property_types'] = all_properties

    if len(argv) == 2 and argv[1].endswith('json'):
        tools.write(schema, argv[1])
    else:
        print tools.print_(schema)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
