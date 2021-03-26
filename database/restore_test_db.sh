#!/bin/bash

cd $(dirname $0)

file=$(basename $1)

if [ -e $file ]; then 
    echo Performing backup of current database to prev.test_db.tar in case you want to rollback
    [ -e prev.test_db.tar ] && rm prev.test_db.tar
    ./backup_test_db.sh prev.test_db.tar

    echo Restore from $file
    docker exec -i --env PGPASSWORD=root pg_container psql -U root -d test_db -v search_path=public -c 'drop schema public cascade'
    docker exec -i --env PGPASSWORD=root pg_container psql -U root -d test_db -v search_path=public -c 'create schema public'

    if [ -e data/admin/storage/$file ]; then
        sudo rm data/admin/storage/$file
    fi
    sudo cp $file data/admin/storage/$file
    sudo chown 5050 data/admin/storage/$file
    sudo chgrp 5050 data/admin/storage/$file

    docker exec -i --env PGPASSWORD=root pgadmin4_container /usr/local/pgsql-13/pg_restore --clean --if-exists -U root --dbname test_db --host pg_container --port 5432 --verbose /var/lib/pgadmin/storage/$file
else
    echo File $file not found
    exit 1
fi
