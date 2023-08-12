# Stop Docker containers
docker container stop $(docker container ls -aq)

# Remove Docker containers, images and volumes
docker container rm -f $(docker container ls -aq)
docker image rm -f $(docker image ls -aq)
docker volume rm -f $(docker volume ls -q)

# Remove migrations directory (and files)
rm -rf migrations

# Remove postgres data directory
rm -rf pgdata

# Create empty migrations directory to avoid errors
mkdir migrations

# Start db container
docker-compose up -d db

# Start app container
docker-compose up -d app

# Start nginx container
docker-compose up -d nginx

# Get app container ID
container_id=$(docker-compose ps -q app)

# Wait for db to be ready
echo "Waiting for the database to be ready..."
while ! docker exec db pg_isready -q; do
  sleep 1
done
echo "Database is ready."

# Initial db migration
docker exec $container_id python manage.py migrate
#docker exec $container_id python manage.py collectstatic --noinput

# Output app container ID
echo "Docker Container ID: $container_id"