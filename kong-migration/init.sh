#!/bin/sh
echo "HEY MAN"

#######################################
# Mock Service
#######################################
SERVICE_NAME="mock_service"
SERVICE_HOST="reqres.in"
SERVICE_PORT="80"
SERVICE_PATH="/api/users"
ROUTE_NAME="mock_route"
ROUTE_PATH="/api/v1/mock"

# Establish service, jwt auth & routing
# /api/v1/mock maps to reqres.in:80/api/users
curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"