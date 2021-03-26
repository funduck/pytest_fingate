#!/bin/bash

cd $(dirname $0)

docker rm -f pg_container
docker rm -f pgadmin4_container
