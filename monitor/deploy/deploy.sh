#!/bin/bash

if [ ! -d "env" ]; then
    virtualenv -p python3.6 env
fi
source env/bin/activate

pip install -r requirements.txt
yarn install

yarn run build

git submodule update --init --recursive

pushd mpstat
patch mpstat.c ../mpstat.patch
./configure && make mpstat
popd

mkdir -p logs
sudo supervisorctl reread
sudo supervisorctl update

sudo supervisorctl restart monitor:
