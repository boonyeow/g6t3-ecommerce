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
amqp_setup.check_setup()


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

        card_details = request.get_json()["card"]

        print("Placing a new order for user:", user_id)
        print("Card details:", card_details)

        result = process_place_an_order(user_id, card_details)

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


def process_place_an_order(user_id, card_details):
    # Call payment microservice to check card
    print("\n-----Invoking payment microservice to check card-----")
    card_results = invoke_http(
        PAYMENT_URL + "/check_card_validity",
        method="GET",
        json={"card": card_details, "customer_email": user_id},
    )
    print(card_results)
    print()

    if card_results["code"] != 200:
        return card_results

    # Call cart microservice to get cart items
    print("\n-----Invoking cart microservice-----")
    cart_result = invoke_http(CART_URL + f"/{user_id}", method="GET")
    print(cart_result)
    print()

    cart_items = cart_result["data"]["items"]
    if cart_result["code"] != 200:
        return cart_result
    if not cart_items:
        return {"code": 400, "message": "Error. No items in cart."}
    products_in_cart_dict = {product["product_id"]: product for product in cart_items}

    print("\n-----Invoking product microservice-----")
    # Call product microservice to check item availability
    product_result = invoke_http(
        PRODUCT_URL + "/get_by_ids",
        method="GET",
        json={"products": list(products_in_cart_dict.keys())},
    )
    print(product_result)
    print()
    if product_result["code"] != 200:
        return product_result

    products_out_of_stock = []

    for product in product_result["data"]:
        stock = product["stock"]
        product_id = product["product_id"]
        customer_qty = products_in_cart_dict[product_id]["quantity"]
        if stock < customer_qty:
            product["user_quantity"] = customer_qty
            products_out_of_stock.append(product)
            del products_in_cart_dict[product_id]
    print(products_out_of_stock)
    print(products_in_cart_dict)
    if products_out_of_stock:
        return {
            "code": 400,
            "data": {
                "cart": list(products_in_cart_dict.values()),
                "removed_items": products_out_of_stock,
            },
            "message": "product out of stock",
        }

    # Call order microservice to place an order
    print("\n-----Invoking order microservice-----")
    order_result = invoke_http(
        ORDER_URL + "/create",
        method="POST",
        json={"user_id": user_id, "items": list(products_in_cart_dict.values())},
    )
    print(order_result)
    print()

    if order_result["code"] != 200:
        return order_result

    # Call payment microservice to pay
    print("\n-----Invoking payment microservice to pay-----")
    payment_amount_cents = round(cart_result["data"]["total_price"] * 100)
    payment_result = invoke_http(
        PAYMENT_URL + "/make_payment",
        method="POST",
        json={"card": card_details, "payment_amount": payment_amount_cents},
    )
    print(payment_result)
    print()

    if payment_result["code"] != 200:
        print("\n-----Invoking order microservice to update order status-----")
        failed_order_results = invoke_http(
            ORDER_URL + f"/failed/{order_result['data']['order_id']}", method="PUT"
        )
        print(failed_order_results)
        print()
        return payment_result

    # Call order microservice to update order status
    print("\n-----Invoking order microservice to update order status-----")
    confirmed_order_results = invoke_http(
        ORDER_URL + f"/complete/{order_result['data']['order_id']}", method="PUT"
    )
    print(confirmed_order_results)
    print()

    if confirmed_order_results["code"] != 200:
        return confirmed_order_results

    # Call product microservice to update product qty
    print("\n-----Invoking product microservice to update product stock-----")
    update_product_stock = invoke_http(
        PRODUCT_URL + "/subtract_stock",
        method="PUT",
        json={
            "products": [
                {
                    "product_id": products_in_cart_dict[product].get("product_id"),
                    "quantity": products_in_cart_dict[product].get("quantity"),
                }
                for product in products_in_cart_dict
            ]
        },
    )
    print(update_product_stock)
    print()

    if update_product_stock["code"] != 200:
        return update_product_stock

    # Call cart microservice to remove purchased items
    new_cart_result = invoke_http(
        CART_URL + f"/clear/{user_id}",
        method="PUT",
    )
    print(new_cart_result)
    print()

    # Call mail microservice to notify
    print("\n-----Invoking mail microservice-----")
    mail = {
        "recipient": user_id,
        "type": "order_processing",
        "order": confirmed_order_results["data"],
    }
    message = json.dumps(mail)
    amqp_setup.channel.basic_publish(
        exchange=amqp_setup.exchangename,
        routing_key="order.mail",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )

    return {"code": 200, "message": "Order successfully placed."}


if __name__ == "__main__":
    print(f"This is flask {os.path.basename(__file__)} for placing an order for a user")
    app.run(host="0.0.0.0", port=5600, debug=True)
