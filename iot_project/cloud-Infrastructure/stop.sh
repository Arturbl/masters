#!/bin/bash

# Stop and remove containers, networks, and volumes, and remove images
docker-compose -f docker-compose.yml down --volumes --rmi all
