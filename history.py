# coding: utf-8
from pyquery import PyQuery as q
import jsonschema
import json
from collections import OrderedDict
h=q('http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html')
false=False
true=True
schema=json.load(open('resource.json'), object_pairs_hook=OrderedDict)
dl = h('#divContent .variablelist dl')
oneOfdict=dict((i['properties']['Type']['pattern'].strip('^$'),i) for i in schema['oneOf'])
pairs=zip(dl('dt'),dl('dd'))
pairs=[(q(dt),q(dd)) for dt,dd in pairs]
oneOfdict['AWS::EC2::CustomerGateway']['properties']['Properties']=dict((dt.text(),{}) for dt,dd in pairs)
required=[k.text() for k,v in pairs if v('p').filter(lambda i: 'Required' in q(this).text() and 'Yes' in q(this).text())]
oneOfdict['AWS::EC2::CustomerGateway']['properties']['Properties']['required']=required
schema['oneOf']=sorted(oneOfdict.values())
with open('resource.json','w') as f: f.write(('\n'.join([l.rstrip() for l in json.dumps(schema, indent=4).splitlines()])))
schema=json.load(open('resource.json'), object_pairs_hook=OrderedDict)
# reorder
pre = h('#divContent pre')
pre=pre.eq(0)
schema=json.load(open('resource.json'), object_pairs_hook=OrderedDict)
current=schema['oneOf'][3]['properties']['Properties']
current['required']=current.pop('required')
with open('resource.json','w') as f: f.write(('\n'.join([l.rstrip() for l in json.dumps(schema, indent=4).splitlines()])))
