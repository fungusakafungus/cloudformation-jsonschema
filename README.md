An attempt to write a json schema (http://json-schema.org) for AWS Cloudformation.

For now, I'm scraping AWS documentation with PyQuery.

This is not your glossy software.

TODO
 - jsonschema
  - specialized validator (the one which will tell you that this resource type is not known)
  - name some features
   - resource types
    - resource types must have Type
    - all resource types should be known
    - unknown resource types are invalid
    - requires resource type properties are desribed
    - missing required resource properties are invalid
 - tests with valid and invalid fragments for every feature
 - define intermediate format for...???
 - define a type for a basic cfn value (string, number or function call object)

cloudformation reference url
 - list of all things, url
 - html for one resource type/property type
