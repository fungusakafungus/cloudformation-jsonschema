#!/usr/bin/env python
import sys
import val
import json

schema = json.load(open('schema.json'))
template = json.load(open(sys.argv[1]))
val.val(template, schema)
