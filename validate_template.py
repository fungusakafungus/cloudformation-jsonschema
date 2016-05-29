#!/usr/bin/env python
import sys
import val
import tools

schema = tools.load('schema.json')
template = tools.load(sys.argv[1])
val.val(template, schema)
