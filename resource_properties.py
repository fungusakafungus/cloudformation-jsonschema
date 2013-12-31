# coding: utf-8
from pyquery import PyQuery as q
import jsonschema
import json
from collections import OrderedDict
from tools import *
from logging import *

def get_type(dd_):
    dd = dd_('p').filter(lambda x: q(this).text().startswith('Type'))
    t = dd.text().lower()
    if 'type : string' in t:
        return {'type': 'string'}
    if 'list of strings' in t:
        return {'type': 'array', 'items': {'type': 'string'}}
    if 'type : integer' in t:
        return {'type': 'integer'}
    if 'type : boolean' in t:
        return {'type': 'boolean'}
    if dd('a'):
        return {'$ref': '#%s' % dd('a').attr('href')}
    if dd_('.type') and len(dd_('.type')):
        if (dd_('.type').text() == 'AWS::EC2::SecurityGroup' and
                'list of' in t):
            return {'type':'array', 'items': {'type':'string'}}

    warn('Could not parse resource property type: "%s"', dd_.html())
    return {}

all_properties = all_resource_properties_hrefs()

def set_resource_properties(res_type):
    all = all_resource_hrefs()
    h=get_pq(all[res_type])
    schema=load()
    dl = h('#divContent .variablelist dl')
    resources=resources_dict(schema)
    pairs=zip(dl('dt'),dl('dd'))
    pairs=[(q(dt),q(dd)) for dt,dd in pairs]
    shortcut = resources[res_type]['properties']
    shortcut['Properties'] = OrderedDict()
    shortcut['Properties']['properties'] = OrderedDict((dt.text(),get_type(dd)) for dt,dd in pairs)
    required=[k.text() for k,v in pairs if v('p').filter(lambda i: 'Required : Yes' in q(this).text())]
    shortcut['Properties']['required']=required
    return schema
