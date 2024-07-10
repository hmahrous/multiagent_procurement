#!/bin/bash

echo "Create application database if not exists"
poetry run python src/scripts/database_init.py

echo "Run migrations"
poetry run alembic upgrade head

echo "Ingesting vector data"
poetry run python src/scripts/ingest_to_db.py
echo "Ingesting vector data complete"