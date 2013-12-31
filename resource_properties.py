# coding: utf-8
from pyquery import PyQuery as q
import jsonschema
import json
from collections import OrderedDict
from tools import *

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
    shortcut['Properties']['properties'] = OrderedDict((dt.text(),{}) for dt,dd in pairs)
    required=[k.text() for k,v in pairs if v('p').filter(lambda i: 'Required : Yes' in q(this).text())]
    shortcut['Properties']['required']=required
    return schema
