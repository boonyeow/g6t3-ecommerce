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
PAYMENT_URL = os.environ.get("PAYMENT_URL") or "http://localhost:5300/order"


@app.route("/place_an_order/<string:user_id>", methods=["POST"])
def place_an_order(user_id):
    try:
        print("Placing a new order for user:", user_id)

        result = process_place_an_order(user_id)

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


def process_place_an_order(user_id):
    # Call cart microservice to get cart items
    print("\n-----Invoking cart microservice-----")
    cart_result = invoke_http(CART_URL + f"/{user_id}", method="GET")
    print(cart_result)
    print()
    cart_items = cart_result["data"]["items"]
    if not cart_items:
        return {"code": 400, "message": "Error. No items in cart."}
    cart_item_ids = [item["product_id"] for item in cart_items]
    product_quantities = {item["product_id"]: item["quantity"] for item in cart_items}

    print("\n-----Invoking product microservice-----")
    # Call product microservice to check item availability
    product_result = invoke_http(
        PRODUCT_URL + "/get_by_ids", method="GET", json={"products": cart_item_ids}
    )
    print(product_result)
    print()
    products = product_result["data"]
    products_out_of_stock = []
    for product in products:
        stock = product["stock"]
        product_id = product["product_id"]
        if stock < product_quantities[product_id]:
            products_out_of_stock.append(product)
    print(products_out_of_stock)

    # Call order microservice to place an order

    # Call payment microservice to pay

    # Call mail microservice to notify

    # Call product microservice to update product qty

    # Call

    return {"code": 200}


if __name__ == "__main__":
    print(f"This is flask {os.path.basename(__file__)} for placing an order for a user")
    app.run(host="0.0.0.0", port=5600, debug=True)
