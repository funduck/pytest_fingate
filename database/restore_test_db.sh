#!/bin/bash

file=$1

echo $file

if [ -e $file ]; then 

    docker exec -i --env PGPASSWORD=root pg_container psql -U root -d test_db -v search_path=public -c 'drop schema public cascade'
    docker exec -i --env PGPASSWORD=root pg_container psql -U root -d test_db -v search_path=public -c 'create schema public'

    sudo rm data/admin/storage/admin_admin.com/$file
    sudo cp $file data/admin/storage/admin_admin.com/$file
    sudo chown 5050 data/admin/storage/admin_admin.com/$file
    sudo chgrp 5050 data/admin/storage/admin_admin.com/$file

    docker exec -i --env PGPASSWORD=root pgadmin4_container /usr/local/pgsql-13/pg_restore --clean --if-exists -U root --dbname test_db --host pg_container --port 5432 --verbose /var/lib/pgadmin/storage/admin_admin.com/$file
fi
