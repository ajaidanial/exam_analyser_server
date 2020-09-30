#!/bin/bash

# This file converts the database schema to an image file

# Convert the schema to a .dot file
docker-compose -f local.yml run django python manage.py graph_models -a >schema_output.dot

# Remove the first line of the .dot file | Contains some unnecessary lines from logging
tail -n +2 "schema_output.dot" >"schema_output.dot.tmp" && mv "schema_output.dot.tmp" "schema_output.dot"

# Convert the .dot file to .png format
dot -Tpng schema_output.dot -o schema_output.png

# Remove the unnecessary .dot file
rm schema_output.dot
