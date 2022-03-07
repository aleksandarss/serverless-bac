#!/bin/bash

# cat files.txt
# changed_files="["
# while IFS= read -r file
# do
#     echo $file
#     changed_files+="${file}, "
# done < files.txt
# echo $changed_files
# changed_files=$(echo $changed_files | sed 's/.$//')
# changed_files="$changed_files]"
# echo $changed_files

infra_deps_files="[infrastructure-deps/cognito/serverless.yml, "

if [[ ${#infra_deps_files} > 2 ]];
then
    infra_deps_files=$(echo $infra_deps_files | sed 's/.$//')
    infra_deps_files="{\"file\": $infra_deps_files]}"
    echo "infra deps files changed!"
    echo $infra_deps_files
    # echo "::set-output name=infra_deps_jobs::$infra_deps_files"
fi