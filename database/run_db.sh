if [ ! -d ./data ]; then
    mkdir -p data/db
    mkdir -p data/admin
    chmod -R 777 data
fi
docker-compose up
