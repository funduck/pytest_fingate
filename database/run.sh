#!/bin/bash

cd $(dirname $0)

if [ ! -d ./data ] || [ ! -d ./data/db ] || [ ! -d ./data/admin ]; then
    mkdir -p data/db
    mkdir -p data/admin
    chmod -R 777 data
fi

docker-compose up -d
