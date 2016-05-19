#!/bin/bash

set -ex

test -z "$1" && { echo Usage: $0 v0.1 >&2; exit 2; }

VERSION=$1
SCHEMA_FILES="schema.json resource.json basic_types.json"

git checkout "$VERSION" -- $SCHEMA_FILES
for f in $SCHEMA_FILES; do
	sed -i -f- $f <<-'SEDSCRIPT'
		1i\
		---\
		---
		3i\
		    "id": "{{site.github.url}}{{page.url}}",
	SEDSCRIPT
done
mkdir -p $VERSION
git mv $SCHEMA_FILES $VERSION
git add $VERSION
