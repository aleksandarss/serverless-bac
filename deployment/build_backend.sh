#!/bin/bash

echo "Building artifacts ..."

for i in */backend/;
     do
          cd $i;
          eval "npm install --production" || exit 1;
          cd ..
     done

