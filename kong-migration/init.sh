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
TARGET_1="auth:5001"
TARGET_2="auth_copy:5001"

UPSTREAM_NAME="auth_upstream"

curl -X POST http://kong:8001/upstreams \
  --data name=${UPSTREAM_NAME}

curl -X POST http://kong:8001/upstreams/${UPSTREAM_NAME}/targets \
  --data target="${TARGET_1}"

curl -X POST http://kong:8001/upstreams/${UPSTREAM_NAME}/targets \
  --data target="${TARGET_2}"

SERVICE_NAME="auth_service"
SERVICE_HOST="auth_upstream"
SERVICE_PORT="80"
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
# Review microservice
#######################################

SERVICE_NAME="review_service"
SERVICE_HOST="review"
SERVICE_PORT="8080"
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

SERVICE_NAME="make_a_review_service"
SERVICE_HOST="make_a_review"
SERVICE_PORT="5200"
SERVICE_PATH="/make_a_review"
ROUTE_NAME="make_a_review_route"
ROUTE_PATH="/api/v1/make_a_review"

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
TARGET_1="order:5300"
TARGET_2="order_copy:5300"
UPSTREAM_NAME="order_upstream"

curl -X POST http://kong:8001/upstreams \
  --data name=${UPSTREAM_NAME}

curl -X POST http://kong:8001/upstreams/${UPSTREAM_NAME}/targets \
  --data target="${TARGET_1}"

curl -X POST http://kong:8001/upstreams/${UPSTREAM_NAME}/targets \
  --data target="${TARGET_2}"

SERVICE_NAME="order_service"
SERVICE_HOST="order_upstream"
SERVICE_PORT="80"
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
# Cart microservice
#######################################

TARGET_1="cart:5500"
TARGET_2="cart_copy:5500"
UPSTREAM_NAME="cart_upstream"

curl -X POST http://kong:8001/upstreams \
  --data name=${UPSTREAM_NAME}

curl -X POST http://kong:8001/upstreams/${UPSTREAM_NAME}/targets \
  --data target="${TARGET_1}"

curl -X POST http://kong:8001/upstreams/${UPSTREAM_NAME}/targets \
  --data target="${TARGET_2}"

SERVICE_NAME="cart_service"
SERVICE_HOST="cart_upstream"
SERVICE_PORT="80"
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




#######################################
# Product microservice
#######################################
TARGET_1="product:5400"
TARGET_2="product_copy:5400"

UPSTREAM_NAME="product_upstream"

curl -X POST http://kong:8001/upstreams \
  --data name=${UPSTREAM_NAME}

curl -X POST http://kong:8001/upstreams/${UPSTREAM_NAME}/targets \
  --data target="${TARGET_1}"

curl -X POST http://kong:8001/upstreams/${UPSTREAM_NAME}/targets \
  --data target="${TARGET_2}"

SERVICE_NAME="product_service"
SERVICE_HOST="product_upstream"
SERVICE_PORT="80"
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

