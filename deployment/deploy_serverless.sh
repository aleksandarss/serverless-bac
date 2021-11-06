#!/bin/bash

# function traverse_directories() {
#     for d in $1 # $(find /mnt/d/Documents/FH_Technikum/Bachelor/app_testing/serverless-bac -maxdepth 1 -type d)
#     do
#         echo "current: $d"
#         traverse_directories "$(ls $(pwd)/$d -d */)" 
#     done
# }

for d in $(pwd)/infrastructure/
do
    echo $d
done

