#!/bin/bash

echo "Building artifacts ..."

cd backend/

for i in */ ; do
     echo "$i"
     cd $i;
     eval "npm install --production" || exit 1;
     cd ..
done
