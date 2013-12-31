# coding: utf-8
# all resource types
from pyquery import PyQuery as q
import jsonschema
import json
from collections import OrderedDict

def load(filename='resource.json'):
    schema=json.load(open('resource.json'), object_pairs_hook=OrderedDict)
    return schema

def get_pq(uri='http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html'):
    h=q(uri)
    h.make_links_absolute()
    return h

def all_resource_hrefs():
    h=get_pq('http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html')
    all_resource_hrefs = OrderedDict([(a.text(), a.attr('href')) for a in [q(a) for a in h('#divContent li a')]])
    return all_resource_hrefs

def write(schema, filename='resource.json'):
    with open('resource.json','w') as f: f.writelines(l.rstrip() + '\n' for l in json.dumps(schema, indent=4).splitlines())

def print_(schema):
    print json.dumps(schema, indent=4)

def all_resource_patterns_by_name():
    h=get_pq('http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html')
    all_resource_patterns_by_name=OrderedDict((a,{'properties':{'Type':{'pattern':'^%s$' % a}}}) for a in h('#divContent li a').map(lambda x: this.text))
    return all_resource_patterns_by_name

def resources_dict(schema):
    o=OrderedDict((i['properties']['Type']['pattern'].strip('^$'), i) for i in schema['oneOf'])
    return o

def update_all_resource_patterns_by_name(schema):
    o=resources_dict()
    new = all_resource_patterns_by_name()
    new.update(o)
    schema['oneOf']=all_resource_patterns_by_name.values()
