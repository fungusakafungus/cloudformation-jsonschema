An attempt to write a json schema (http://json-schema.org) for AWS Cloudformation.

For now, I'm scraping AWS documentation with PyQuery.

This is not your glossy software.

### current state
Many things are validated, but some are not: attributes and resource property types are not validated yet.
Some resource properties are not parsed properly.

### how to use
Use `./validate_template.py tests/examples-aws/Rails_Single_Instance.template` to validate cloudformation templates on command line.

Use `schema.json` programmatically to validate complete Cloudformation templates.

Use `resource.json` to validate one resource.

The schema consists of multiple files, `schema.json`, `resource.json` and `basic_types.json`. To resolve JSON pointers (`{"$ref": "basic_types.json#/definitions/string"}`) to files on local filesystem, you'll have to use a special resolver. See `val.py` for the example.

### how to contribute
Create a virtualenv (`virtualenv venv; pip install -r requirements.txt`)

You can then scrape AWS documentation for cloudformation resource types and save it as jsonschema:

```
./create_resource_schema.py resource.json
```

### TODO
 - [x] specialized validator (the one which will tell you that this resource type is not known)
 - [x] tests with valid and invalid fragments for every feature. See `tests/test_stage1_valid.py`
 - [x] define a type for a basic cfn value (string, number or function call(Ref, Join) object)
  - [x] Fn::Base64
  - [x] Condition Functions
  - [x] Fn::FindInMap
  - [x] Fn::GetAtt
  - [x] Fn::GetAZs
  - [x] Fn::Join
  - [x] Fn::Select
  - [x] Ref
  - [x] number
  - [x] string
 - [x] integrate/link schema.json and resource.json
 - [x] travis/circleci
 - [ ] validate resource property types (listed here: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-product-property-reference.html)
 - [ ] validate attributes (`Metadata`, `UpdatePolicy` and others)
 - [ ] make json objects more stable (use more OrderedDict)

cloudformation reference url
 - list of all things, url
 - html for one resource type/property type
