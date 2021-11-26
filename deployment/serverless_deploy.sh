#!/bin/bash

echo "Deploying backend artifacts ..."

cd $FOLDER

for i in */ ; do
     echo "$i"
     cd $i;
     eval "serverless deploy --stage dev" || exit 1;
     cd ..
done