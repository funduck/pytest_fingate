#!/bin/bash

cd $(dirname $0)

file=$(basename $1)

if [ ! -e $file ]; then 
    echo Backup to $file

    docker exec -i --env PGPASSWORD=root pgadmin4_container /usr/local/pgsql-13/pg_dump -U root --dbname test_db --host pg_container --port 5432 --verbose --format=t -f /var/lib/pgadmin/storage/$file

    if [ -e data/admin/storage/$file ]; then
        sudo mv data/admin/storage/$file $file
        sudo chown `whoami` $file
    fi
else
    echo Remove file $file before backup
    exit 1
fi

