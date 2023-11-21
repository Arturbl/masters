REM Stop and remove the containers
docker-compose down

REM Remove the images
docker-compose rm -f

REM Prune unused images (optional, use with caution)
docker image prune -a -f
