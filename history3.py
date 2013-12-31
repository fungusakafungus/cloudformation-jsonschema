# coding: utf-8
with open('resource.json','w') as f: f.writelines(l.rstrip() + '\n' for l in json.dumps(schema, indent=4).splitlines())