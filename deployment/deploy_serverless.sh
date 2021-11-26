#!/bin/bash

# function traverse_directories() {
#     for d in $1 # $(find /mnt/d/Documents/FH_Technikum/Bachelor/app_testing/serverless-bac -maxdepth 1 -type d)
#     do
#         echo "current: $d"
#         traverse_directories "$(ls $(pwd)/$d -d */)" 
#     done
# }

array=()

array+=(1)
array+=(2)

for value in "${array[@]}"
do
     echo $value
done

