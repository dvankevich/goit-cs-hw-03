#!/bin/bash

CONTAINER_NAME="task01-postgres"
POSTGRES_PASSWORD="mysecretpassword"
SQL_FILE="createdb.sql"

docker run --name $CONTAINER_NAME -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -p 5432:5432 -d postgres

echo "Waiting for PostgreSQL to start..."
until docker exec $CONTAINER_NAME pg_isready -U postgres > /dev/null 2>&1; do
  echo -n "."
  sleep 2
done


cat $SQL_FILE | docker exec -i $CONTAINER_NAME psql -U postgres

echo "Tables created successfully."