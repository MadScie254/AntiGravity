#!/bin/bash
# Seed script for loading demo data

set -e

echo "Running migrations..."
python manage.py migrate

echo "Loading seed data..."
python manage.py seed_data

echo "Seed complete!"
