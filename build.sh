#!/usr/bin/env bash

build () {
  SCRIPT_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
  pushd $SCRIPT_DIRECTORY > /dev/null

  rm -rf .package python_function.zip
  mkdir .package

  pip3 install --target .package .

  pushd .package > /dev/null
  zip --recurse-paths ${SCRIPT_DIRECTORY}/python_function.zip .
  popd > /dev/null
}

# Check if on 'master' branch by parsing the provided environemnt variable. The branch name is empty for master branch.
if [ -z "$BRANCH_NAME" ]; then
  echo "On master branch. Starting build."
  build
  echo "Uploading."
  aws s3 cp python_function.zip s3://bwijayaw-riiid-production --acl bucket-owner-full-control
else
  echo "On branch: ${BRANCH_NAME}. Starting build."
  build
  echo "Upload skipped due to non-master branch."
fi

