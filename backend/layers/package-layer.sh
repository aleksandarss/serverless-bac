#!/bin/bash

export PKG_DIR="db-layer-new/python"

rm -rf ${PKG_DIR} && mkdir -p ${PKG_DIR}

docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 \
    pip install -r db-layer-new/requirements.txt --no-deps -t ${PKG_DIR}