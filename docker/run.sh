#!/bin/sh

echo "Alembic start"
make alembic
echo "Alembic success"

echo "Python start"
make run
