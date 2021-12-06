#!/bin/bash

set -e

if [ "${AIRFLOW_UPGRADE_DB}x" != "x" ]; then
  PGPASSWORD=postgres psql -v ON_ERROR_STOP=1 --username postgres --host postgres <<-EOSQL
  SELECT 'CREATE DATABASE airflow' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow')\gexec
  GRANT ALL PRIVILEGES ON DATABASE airflow TO postgres;
EOSQL

  airflow upgradedb

  airflow connections \
    --add \
    --conn_id 'postgres_db' \
    --conn_uri 'postgres://postgres:postgres@postgres:5432/airflow'

fi

exec "$@"
