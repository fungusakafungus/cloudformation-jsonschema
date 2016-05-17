An attempt to write a json schema (http://json-schema.org) for AWS Cloudformation.

For now, I'm scraping AWS documentation with PyQuery.

This is not your glossy software.

### how to use
Use `schema.json` to validate complete Cloudformation templates.

Use `resource.json` to validate a particular resource.

### how to contribute
Create a virtualenv (`virtualenv venv; pip install -r requirements.txt`)

You can then scrape AWS documentation for cloudformation resource types and save it as jsonschema:

```
./create_resource_schema.py resource.json
```

### TODO
 - [ ] specialized validator (the one which will tell you that this resource type is not known)
 - [ ] tests with valid and invalid fragments for every feature
 - [ ] define a type for a basic cfn value (string, number or function call(Ref, Join) object)
  - [x] Fn::Base64
  - [ ] Condition Functions
  - [x] Fn::FindInMap
  - [x] Fn::GetAtt
  - [ ] Fn::GetAZs
  - [ ] Fn::Join
  - [ ] Fn::Select
  - [x] Ref
  - [x] number
  - [x] string
 - [ ] integrate/link schema.json and resource.json
 - [x] travis/circleci
 - [ ] scrape Resource Property Types from http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-product-property-reference.html
 - [ ] make json objects more stable (use more OrderedDict)

cloudformation reference url
 - list of all things, url
 - html for one resource type/property type
