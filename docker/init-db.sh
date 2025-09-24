#!/bin/bash
set -e

# Create multiple databases for Temporal
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE temporal_visibility;
    GRANT ALL PRIVILEGES ON DATABASE temporal_visibility TO $POSTGRES_USER;
EOSQL

echo "Temporal databases created successfully!"
