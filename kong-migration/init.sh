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


#######################################
# Auth Service
#######################################
SERVICE_NAME="auth_service"
SERVICE_HOST="auth"
SERVICE_PORT="5001"
SERVICE_PATH=""
ROUTE_NAME="auth_route"
ROUTE_PATH="/api/v1/auth"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"

#######################################
# Product Service
#######################################

SERVICE_NAME="product_service"
SERVICE_HOST="product"
SERVICE_PORT="5400"
SERVICE_PATH="/product"
ROUTE_NAME="product_route"
ROUTE_PATH="/api/v1/product"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \
    
curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"


#######################################
# Review microservice
#######################################

SERVICE_NAME="review_service"
SERVICE_HOST="review"
SERVICE_PORT="5100"
SERVICE_PATH="/review"
ROUTE_NAME="review_route"
ROUTE_PATH="/api/v1/review"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \
    
curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"

#######################################
# Make review microservice
#######################################

SERVICE_NAME="make_review_service"
SERVICE_HOST="make_review"
SERVICE_PORT="5200"
SERVICE_PATH="/make_review"
ROUTE_NAME="make_review_route"
ROUTE_PATH="/api/v1/make_review"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \
    
curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"


#######################################
# Order microservice
#######################################

SERVICE_NAME="order_service"
SERVICE_HOST="order"
SERVICE_PORT="5300"
SERVICE_PATH="/order"
ROUTE_NAME="order_route"
ROUTE_PATH="/api/v1/order"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \
    
curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"
  
#######################################
# Product microservice
#######################################

SERVICE_NAME="product_service"
SERVICE_HOST="product"
SERVICE_PORT="5400"
SERVICE_PATH="/product"
ROUTE_NAME="product_route"
ROUTE_PATH="/api/v1/product"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \
    
curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"

#######################################
# Cart microservice
#######################################

SERVICE_NAME="cart_service"
SERVICE_HOST="cart"
SERVICE_PORT="5500"
SERVICE_PATH="/cart"
ROUTE_NAME="cart_route"
ROUTE_PATH="/api/v1/cart"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"

#######################################
# Product notification microservice
#######################################

SERVICE_NAME="place_an_order_service"
SERVICE_HOST="place_an_order"
SERVICE_PORT="5600"
SERVICE_PATH="/place_an_order"
ROUTE_NAME="place_an_order_route"
ROUTE_PATH="/api/v1/place_an_order"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"

#######################################
# Payment microservice
#######################################

SERVICE_NAME="payment_service"
SERVICE_HOST="payment"
SERVICE_PORT="5700"
SERVICE_PATH="/payment"
ROUTE_NAME="payment_route"
ROUTE_PATH="/api/v1/payment"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"

#######################################
# Product notification microservice
#######################################

SERVICE_NAME="product_notification_service"
SERVICE_HOST="product_notification"
SERVICE_PORT="5800"
SERVICE_PATH="/product_notification"
ROUTE_NAME="product_notification_route"
ROUTE_PATH="/api/v1/product_notification"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"

#######################################
# Add to cart microservice
#######################################

SERVICE_NAME="add_to_cart_service"
SERVICE_HOST="add_to_cart"
SERVICE_PORT="5900"
SERVICE_PATH="/add_to_cart"
ROUTE_NAME="add_to_cart_route"
ROUTE_PATH="/api/v1/add_to_cart"

curl -i -X POST http://kong:8001/services \
    --data "name=${SERVICE_NAME}" \
    --data "url=http://${SERVICE_HOST}:${SERVICE_PORT}${SERVICE_PATH}"

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=jwt" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/plugins \
    --data "name=cors" \

curl -i -X POST http://kong:8001/services/${SERVICE_NAME}/routes \
  --data "paths[]=${ROUTE_PATH}" \
  --data "name=${ROUTE_NAME}"