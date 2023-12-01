#!/bin/bash

cd ..

# Stop and remove the containers
docker-compose down

# Remove the images
docker-compose rm -f

# Prune unused images (optional, use with caution)
docker image prune -a -f
