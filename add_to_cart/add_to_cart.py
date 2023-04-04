from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os
import sys

# Flask config
app = Flask(__name__)
CORS(app)

# URLs
PRODUCT_URL = os.environ.get("PRODUCT_URL") or "http://localhost:5400/product"
CART_URL = os.environ.get("CART_URL") or "http://localhost:5500/cart"


@app.route("/add_to_cart/<string:user_id>", methods=["POST"])
def add_to_cart(user_id):
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

        product_object = request.get_json()

        print("Adding to cart for user:", user_id)
        print("Item details:", product_object)

        result = process_add_to_cart(user_id, product_object)

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


def process_add_to_cart(user_id, product_object):
    print("\n-----Invoking cart microservice to get user's current cart-----")
    cart_result = invoke_http(CART_URL + f"/{user_id}", method="GET")
    print(cart_result)
    print()
    product_current_qty = 0
    for product in cart_result["data"]["items"]:
        if product["product_id"] == product_object["product_id"]:
            product_current_qty = product["quantity"]

    print("\n-----Invoking product microservice to check product stock-----")
    product_result = invoke_http(PRODUCT_URL + f"/get/{product_object['product_id']}")
    print(product_result)
    print()
    if product_result["code"] != 200:
        return product_result
    if (
        product_result["data"]["stock"]
        < product_object["quantity"] + product_current_qty
    ):
        return {
            "code": 409,
            "message": "Not enough stock available.",
            "data": cart_result["data"],
        }

    print("\n-----Invoking cart microservice to add product to cart-----")
    new_cart_result = invoke_http(
        CART_URL + f"/add_item_to_cart/{user_id}", method="PUT", json=product_object
    )
    print(new_cart_result)
    print()

    return new_cart_result


if __name__ == "__main__":
    print(
        f"This is flask {os.path.basename(__file__)} for adding an item to cart for a user"
    )
    app.run(host="0.0.0.0", port=5900, debug=True)
