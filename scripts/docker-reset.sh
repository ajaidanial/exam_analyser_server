#!/bin/bash

# stop and remove containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
# remove volumes
docker volume prune
# remove images
docker rmi $(docker images -a -q) -f
