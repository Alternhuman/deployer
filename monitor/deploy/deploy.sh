#!/bin/bash

if [ ! -d "env" ]; then
    virtualenv -p python3.6 env
fi
source env/bin/activate

pip install -r requirements.txt
yarn install

yarn run build
