#! /usr/bin/env sh

# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head
# Start flask
flask run --host=0.0.0.0 --port=8000