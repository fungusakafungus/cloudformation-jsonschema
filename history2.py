# coding: utf-8
# all resource types
h=q('http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html')
h.make_links_absolute()
o=OrderedDict((i['properties']['Type']['pattern'].strip('^$'), i) for i in schema['oneOf'])
all_resource_hrefs=OrderedDict([(a.text(), a.attr('href')) for a in [q(a) for a in h('#divContent li a')]])
all_resource_patterns_by_name=OrderedDict((a,{'properties':{'Type':{'pattern':'^%s$' % a}}}) for a in h('#divContent li a').map(lambda x: this.text))
all_resource_patterns_by_name.update(o)
schema['oneOf']=all_resource_patterns_by_name.values()
with open('resource.json','w') as f: f.write(('\n'.join([l.rstrip() for l in json.dumps(schema, indent=4).splitlines()])))
