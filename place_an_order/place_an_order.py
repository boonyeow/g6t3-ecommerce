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


@app.route("/place_an_order", methods=["POST"])
def place_an_order():
    """
    This is the function that handles placing a new order
    Format of request body:
    {
        "user_id"
    }
    """
    if not request.is_json:
        return (
            jsonify(
                {
                    "code": 400,
                    "message": "Invalid JSON request body: " + str(request.get_data()),
                }
            ),
            400,
        )

    try:
        request_body = request.get_json()
        print("request_body:", request_body)

        result = process_place_an_order(request_body)

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


def process_place_an_order(request_body):
    