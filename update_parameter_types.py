#!/usr/bin/env python

import tools
import resource_properties
import val

import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


def parse_paremeter_types(dd):
    from pyquery import PyQuery as q
    from collections import OrderedDict
    types = [q(dt).text() for dt in dd('dl dt')]
    result = OrderedDict()
    result['type'] = 'string'
    result['enum'] = types

    return result


def parse_parameters():
    from pyquery import PyQuery as q
    from collections import OrderedDict
    parameters_href = tools.BASE + 'parameters-section-structure.html'
    h = tools.get_pq(parameters_href)
    dl = h('#main-col-body .variablelist dl').eq(0)
    dl = q(dl)
    dl = zip(dl.children('dt'), dl.children('dd'))
    dl = OrderedDict((q(dt).text(), q(dd)) for dt, dd in dl)
    result = OrderedDict()
    result['Type'] = parse_paremeter_types(dl.pop('Type'))
    for dt in dl.keys():
        result[dt] = {'type': 'string'}
    return result


def main(argv):
    sess = CacheControl(requests.Session(),
                        cache=FileCache('.web_cache'))
    requests.get = sess.get

    schema = tools.load('schema.json')
    schema['definitions']['Parameter']['properties'] = parse_parameters()
    tools.write(schema, 'schema.json')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
