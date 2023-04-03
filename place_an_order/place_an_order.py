from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os, sys
import json
import amqp_setup
import pika

app = Flask(__name__)
CORS(app)

CART_URL = os.environ.get("CART_URL") or "http://localhost:5500/cart"
PRODUCT_URL = os.environ.get("PRODUCT_URL") or "http://localhost:5400/product"
ORDER_URL = os.environ.get("ORDER_URL") or "http://localhost:5300/order"
PAYMENT_URL = os.environ.get("PAYMENT_URL") or "http://localhost:5700/payment"


@app.route("/place_an_order/<string:user_id>", methods=["POST"])
def place_an_order(user_id):
    try:
        if not request.is_json:
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "Invalid JSON request body" + str(request.get_data),
                    }
                ),
                400,
            )

        request_body = request.get_json()

        print("Placing a new order for user:", user_id)
        print("Checking out the following items:", request_body["product_ids"])

        result = process_place_an_order(user_id, set(request_body["product_ids"]))

        return jsonify(result), result["code"]

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        exception_str = f"{str(e)} at {exc_type}: {fname} : line {exc_tb.tb_lineno}"
        print(exception_str)

        return (
            jsonify({"code": 500, "message": fname + " error: " + exception_str}),
            500,
        )


def process_place_an_order(user_id, product_ids_to_checkout):
    # Call cart microservice to get cart items
    print("\n-----Invoking cart microservice-----")
    cart_result = invoke_http(CART_URL + f"/{user_id}", method="GET")
    print(cart_result)
    print()
    cart_items = cart_result["data"]["items"]
    if not cart_items:
        return {"code": 400, "message": "Error. No items in cart."}
    products_to_checkout = {
        item["product_id"]: item
        for item in cart_items
        if item["product_id"] in product_ids_to_checkout
    }

    print("\n-----Invoking product microservice-----")
    # Call product microservice to check item availability
    product_result = invoke_http(
        PRODUCT_URL + "/get_by_ids",
        method="GET",
        json={"products": list(product_ids_to_checkout)},
    )
    print(product_result)
    print()
    products_out_of_stock = []
    for product in product_result["data"]:
        stock = product["stock"]
        product_id = product["product_id"]
        if product_id not in products_to_checkout:
            return {"code": 404, "message": f"Product not in cart: {product_id}"}
        if stock < products_to_checkout[product_id]["quantity"]:
            products_out_of_stock.append(product)
            del products_to_checkout[product_id]
    if products_out_of_stock:
        return {
            "code": 400,
            "data": {
                "cart": list(products_to_checkout.values()),
                "removed_items": products_out_of_stock,
            },
            "message": "product out of stock",
        }

    # Call order microservice to place an order
    print("\n-----Invoking order microservice-----")
    order_result = invoke_http(
        ORDER_URL + "/create",
        method="POST",
        json={"user_id": user_id, "items": list(products_to_checkout.values())},
    )
    print(order_result)
    print()
    if order_result["code"] != 200:
        return {"code": 500, "message": "Failed to create order."}

    # Call payment microservice to pay
    print("\n-----Invoking payment microservice-----")
    payment_response = invoke_http(PAYMENT_URL + "/checkout", method="POST")
    print(payment_response)
    print(payment_response["payment_link"])

    # Call mail microservice to notify

    # Call product microservice to update product qty

    # Call

    return {"code": 200}


if __name__ == "__main__":
    print(f"This is flask {os.path.basename(__file__)} for placing an order for a user")
    app.run(host="0.0.0.0", port=5600, debug=True)
