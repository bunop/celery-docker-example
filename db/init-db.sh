#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    -- Creating test user
    CREATE USER django PASSWORD 'django_password';

    -- Assigning privileges to 'django'
    ALTER USER django CREATEDB;

    -- Creating image database
    CREATE DATABASE django;

    -- Assigning privileges to database (public schema)
    GRANT ALL PRIVILEGES ON DATABASE django TO django;
EOSQL
