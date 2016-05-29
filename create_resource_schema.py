#!/usr/bin/env python

import tools
import resource_properties
import tweak_resource_schema

import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
import argparse


def main(argv):
    parser = argparse.ArgumentParser(description='Create or update cfn resource schema')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--type', metavar='TYPE',
                        help='Restrict parsing resource type properties only to'
                        ' type TYPE. Example: --type AWS::ApiGateway::RestApi')
    parser.add_argument('--source', '-s', metavar='FILE',
                        default='resource-stage1.json',
                        help='Source/skeleton/stage1 for resource schema')
    parser.add_argument('dest', nargs='?', help='Write resulting schema into FILE'
                        ' instead of just printing it')

    args = parser.parse_args(argv[1:])

    sess = CacheControl(requests.Session(),
                        cache=FileCache('.web_cache'))
    requests.get = sess.get

    resource_schema = tools.load(args.source)

    resource_type_names = tools.get_all_resource_type_names()
    tools.update_all_resource_patterns_by_name(
        resource_schema,
        resource_type_names
    )

    if args.type:
        resource_type_names = [args.type]

    for resource_type_name in resource_type_names:
        print >> sys.stderr, resource_type_name
        resource_properties.set_resource_properties(resource_schema, resource_type_name)

    del resource_schema['definitions']['resource_template']

    all_properties = resource_properties.all_res_properties()
    resource_schema['definitions']['property_types'] = all_properties

    tweak_resource_schema.apply_all_tweaks(resource_schema)

    if args.dest:
        tools.write(resource_schema, args.dest)
    else:
        print tools.print_(resource_schema)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
