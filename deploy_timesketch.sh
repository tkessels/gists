#!/bin/bash

# Create dirs
mkdir -p timesketch/{data/postgresql,data/elasticsearch,logs,etc,etc/timesketch,etc/timesketch/sigma/rules,upload}

echo -n "* Setting default config parameters.."
POSTGRES_USER="timesketch"
POSTGRES_PASSWORD="$(< /dev/urandom tr -dc A-Za-z0-9 | head -c 32 ; echo)"
POSTGRES_ADDRESS="postgres"
POSTGRES_PORT=5432
SECRET_KEY="$(< /dev/urandom tr -dc A-Za-z0-9 | head -c 32 ; echo)"
ELASTIC_ADDRESS="elasticsearch"
ELASTIC_PORT=9200
REDIS_ADDRESS="redis"
REDIS_PORT=6379
GITHUB_BASE_URL="https://raw.githubusercontent.com/google/timesketch/master"
ELASTIC_MEM_USE_GB=$(cat /proc/meminfo | grep MemTotal | awk '{printf "%.0f", ($2 / 1000000 / 2)}')
echo "OK"
echo "* Setting Elasticsearch memory allocation to ${ELASTIC_MEM_USE_GB}GB"

# Docker compose and configuration
echo -n "* Fetching configuration files.."
curl  $GITHUB_BASE_URL/docker/release/docker-compose.yml > timesketch/docker-compose.yml
curl  $GITHUB_BASE_URL/docker/release/config.env > timesketch/config.env

# Fetch default Timesketch config files
curl  $GITHUB_BASE_URL/data/timesketch.conf > timesketch/etc/timesketch/timesketch.conf
curl  $GITHUB_BASE_URL/data/tags.yaml > timesketch/etc/timesketch/tags.yaml
curl  $GITHUB_BASE_URL/data/plaso.mappings > timesketch/etc/timesketch/plaso.mappings
curl  $GITHUB_BASE_URL/data/generic.mappings > timesketch/etc/timesketch/generic.mappings
curl  $GITHUB_BASE_URL/data/features.yaml > timesketch/etc/timesketch/features.yaml
curl  $GITHUB_BASE_URL/data/sigma_config.yaml > timesketch/etc/timesketch/sigma_config.yaml
curl  $GITHUB_BASE_URL/data/sigma/rules/lnx_susp_zenmap.yml > timesketch/etc/timesketch/sigma/rules/lnx_susp_zenmap.yml
curl  $GITHUB_BASE_URL/contrib/nginx.conf > timesketch/etc/nginx.conf
echo "OK"

# Create a minimal Timesketch config
echo -n "* Edit configuration files.."
sed -i 's#SECRET_KEY = \x27\x3CKEY_GOES_HERE\x3E\x27#SECRET_KEY = \x27'$SECRET_KEY'\x27#' timesketch/etc/timesketch/timesketch.conf

# Set up the Elastic connection
sed -i 's#^ELASTIC_HOST = \x27127.0.0.1\x27#ELASTIC_HOST = \x27'$ELASTIC_ADDRESS'\x27#' timesketch/etc/timesketch/timesketch.conf
sed -i 's#^ELASTIC_PORT = 9200#ELASTIC_PORT = '$ELASTIC_PORT'#' timesketch/etc/timesketch/timesketch.conf

# Set up the Redis connection
sed -i 's#^UPLOAD_ENABLED = False#UPLOAD_ENABLED = True#' timesketch/etc/timesketch/timesketch.conf
sed -i 's#^UPLOAD_FOLDER = \x27/tmp\x27#UPLOAD_FOLDER = \x27/usr/share/timesketch/upload\x27#' timesketch/etc/timesketch/timesketch.conf

sed -i 's#^CELERY_BROKER_URL =.*#CELERY_BROKER_URL = \x27redis://'$REDIS_ADDRESS':'$REDIS_PORT'\x27#' timesketch/etc/timesketch/timesketch.conf
sed -i 's#^CELERY_RESULT_BACKEND =.*#CELERY_RESULT_BACKEND = \x27redis://'$REDIS_ADDRESS':'$REDIS_PORT'\x27#' timesketch/etc/timesketch/timesketch.conf

# Set up the Postgres connection
sed -i 's#postgresql://<USERNAME>:<PASSWORD>@localhost#postgresql://'$POSTGRES_USER':'$POSTGRES_PASSWORD'@'$POSTGRES_ADDRESS':'$POSTGRES_PORT'#' timesketch/etc/timesketch/timesketch.conf

sed -i 's#^POSTGRES_PASSWORD=#POSTGRES_PASSWORD='$POSTGRES_PASSWORD'#' timesketch/config.env
sed -i 's#^ELASTIC_MEM_USE_GB=#ELASTIC_MEM_USE_GB='$ELASTIC_MEM_USE_GB'#' timesketch/config.env

ln -s ./config.env ./timesketch/.env
echo "OK"
echo "* Installation done."

echo
echo "Start the system:"
echo "1. cd timesketch"
echo "2. docker-compose up -d"
echo "3. docker-compose exec timesketch-web tsctl add_user --username <USERNAME>"
echo
echo "WARNING: The server is running without encryption."
echo "Follow the instructions to enable SSL to secure the communications:"
echo "https://github.com/google/timesketch/blob/master/docs/Installation.md"
echo
echo
