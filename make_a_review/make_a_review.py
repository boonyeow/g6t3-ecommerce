from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import amqp_setup
import json
import os
import sys
import pika

app = Flask(__name__)
CORS(app)

REVIEW_URL = os.environ.get("REVIEW_URL") or "http://localhost:5100/review"
ORDER_URL = os.environ.get("ORDER_URL") or "http://localhost:5300/order"
PRODUCT_URL = os.environ.get("PRODUCT_URL") or "http://localhost:5400/product"


@app.route("/make_a_review", methods=["POST"])
def make_a_review():
    """
    This is the function that handles making a new review
    format of a review:
    {
        product_id,
        order_id,
        user_id,
        review_description,
        review_stars
    }
    """
    if request.is_json:
        try:
            review = request.get_json()
            print("New Review:", review)

            result = process_make_review(review)

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
    return (
        jsonify(
            {
                "code": 400,
                "message": "Invalid JSON request body: " + str(request.get_data()),
            }
        ),
        400,
    )


def process_make_review(review):
    # Call order microservice to get order_date
    print("\n-----Invoking order microservice-----")
    order_result = invoke_http(ORDER_URL + "/get/" + review["order_id"], method="GET")
    print(order_result)
    print()
    if order_result["code"] != 200:
        return order_result
    if order_result["data"]["user_id"] != review["user_id"]:
        return {"code": 404, "message": "Incorrect user for the order"}
    products_in_order = [item["product_id"] for item in order_result["data"]["items"]]
    if review["product_id"] not in products_in_order:
        return {"code": 404, "message": "Product not in order"}
    review["purchase_date"] = order_result["data"]["time"]

    print("\n-----Invoking review microservice-----")
    review_result = invoke_http(REVIEW_URL, method="POST", json=review)
    print(review_result)
    print()
    if review_result["code"] != 200 or int(review["review_stars"]) >= 3:
        return review_result

    print("\n-----Invoking product microservice-----")
    product_result = invoke_http(PRODUCT_URL + "/get/" + review["product_id"])
    print(product_result)
    print()
    if product_result["code"] != 200:
        return product_result
    seller_email = product_result["data"]["seller_email"]

    print("\n-----Invoking mail microservice-----")
    mail = {
        "recipient": seller_email,
        "type": "bad_review",
        "product_name": product_result["data"]["product_name"],
        "product_id": product_result["data"]["product_id"],
        "user_id": review_result["data"]["user_id"],
        "review_stars": review["review_stars"],
        "review_description": review["review_description"],
    }
    message = json.dumps(mail)
    amqp_setup.check_setup()
    amqp_setup.channel.basic_publish(
        exchange=amqp_setup.exchangename,
        routing_key="review.mail",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )

    return {"code": 200, "message": review_result["message"]}


if __name__ == "__main__":
    print(
        "This is flask "
        + os.path.basename(__file__)
        + " for making a review for a product."
    )
    app.run(host="0.0.0.0", port=5200, debug=True)
