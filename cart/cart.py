from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

# DB Configuration
URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_db_connection = MongoClient(URI)
cart_database = mongo_db_connection["cart"]
cart_collection = cart_database["cart_details"]

# Flask Configuration
app = Flask(__name__)
CORS(app)


def calculate_cart_total(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item["price"] * item["quantity"]
    return total_price


def check_valid_product_request(product):
    if (
        not product.get("product_id")
        or not product.get("product_name")
        or not product.get("price")
        or not product.get("seller_email")
        or product.get("quantity") == None
        or not product.get("image_url")
    ):
        return False
    return True


@app.route("/cart/<string:user_id>")
def get_cart_by_user_id(user_id):
    try:
        cart = cart_collection.find_one({"user_id": user_id})
        if not cart:
            new_cart = {"user_id": user_id, "items": [], "total_price": 0}
            cart_collection.insert_one(new_cart)
            del new_cart["_id"]
            return jsonify({"code": 200, "data": new_cart}), 200

        del cart["_id"]

        return jsonify({"code": 200, "data": cart}), 200
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/cart/add_item_to_cart/<string:user_id>", methods=["PUT"])
def add_item_to_user_cart(user_id):
    try:
        if not request.is_json:
            return jsonify(
                {
                    "code": 400,
                    "message": "Invalid JSON request body provided:"
                    + str(request.get_data()),
                }
            )

        request_body = request.get_json()
        if not check_valid_product_request(request_body):
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "Incomplete JSON request body provided:"
                        + str(request_body),
                    }
                ),
                400,
            )

        cart = cart_collection.find_one({"user_id": user_id})

        if not cart:
            cart = {"user_id": user_id, "items": [], "total_price": 0}
            cart_collection.insert_one(cart)

        product_id = request_body.get("product_id")
        quantity = request_body.get("quantity")

        item_already_in_cart = False
        for i in range(len(cart["items"])):
            item = cart["items"][i]
            if product_id == item["product_id"]:
                item_already_in_cart = True

                # Changes item qty directly
                item["quantity"] += quantity
                if item["quantity"] <= 0:
                    cart["items"].pop(i)
                break

        if not item_already_in_cart:
            if quantity < 0:
                return jsonify(
                    {
                        "code": 400,
                        "message": "Cannot have negative item quantity in cart",
                    }
                )
            else:
                product_name = request_body.get("product_name")
                price = request_body.get("price")
                seller_email = request_body.get("seller_email")
                image_url = request_body.get("image_url")
                cart["items"].append(
                    {
                        "product_id": product_id,
                        "product_name": product_name,
                        "price": price,
                        "seller_email": seller_email,
                        "quantity": quantity,
                        "image_url": image_url,
                    }
                )

        cart["total_price"] = calculate_cart_total(cart["items"])
        print(cart)

        cart_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "items": cart["items"],
                    "total_price": round(cart["total_price"], 2),
                }
            },
        )

        del cart["_id"]

        return jsonify({"code": 200, "data": cart}), 200
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/cart/remove/<string:user_id>/<string:product_id>", methods=["PUT"])
def remove_item_from_cart(user_id, product_id):
    try:
        cart = cart_collection.find_one({"user_id": user_id})
        if not cart:
            return jsonify({"code": 404, "message": "Cart not found."}), 404

        del cart["_id"]

        item_index = None
        for i in range(len(cart["items"])):
            cart_item = cart["items"][i]
            if cart_item["product_id"] == product_id:
                item_index = i
                break

        if item_index == None:
            return jsonify({"code": 404, "message": "Item does not exist in cart"}), 404

        cart["items"].pop(item_index)

        cart["total_price"] = calculate_cart_total(cart["items"])

        cart_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "items": cart["items"],
                    "total_price": round(cart["total_price"], 2),
                }
            },
        )

        return jsonify({"code": 200, "data": cart}), 200
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/cart/remove_items/<string:user_id>", methods=["PUT"])
def remove_items_from_cart(user_id):
    try:
        cart = cart_collection.find_one({"user_id": user_id})
        if not cart:
            return jsonify({"code": 404, "message": "Cart not found."}), 404

        del cart["_id"]

        if not request.is_json:
            return (
                jsonify({"code": 400, "message": "Invalid request body provided"}),
                400,
            )

        request_body = request.get_json()
        if not request_body.get("product_ids"):
            return jsonify(
                {
                    "code": 400,
                    "message": "Incorrect JSON request body. 'product_ids' is a required key."
                    + str(request_body),
                }
            )

        product_ids = set(request_body.get("product_ids"))
        new_cart_items = [
            item for item in cart["items"] if item["product_id"] not in product_ids
        ]

        cart["items"] = new_cart_items

        cart["total_price"] = calculate_cart_total(cart["items"])

        cart_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "items": cart["items"],
                    "total_price": round(cart["total_price"], 2),
                }
            },
        )

        return jsonify({"code": 200, "data": cart}), 200
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/cart/set/<string:user_id>", methods=["PUT"])
def set_cart_items(user_id):
    try:
        if not request.is_json:
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "Invalid JSON request body provided:"
                        + str(request.get_data()),
                    }
                ),
                400,
            )

        request_body = request.get_json()
        for product in request_body:
            if not check_valid_product_request(product):
                return (
                    jsonify(
                        {
                            "code": 400,
                            "message": "Incomplete JSON request body provided:"
                            + str(request_body),
                        }
                    ),
                    400,
                )

        cart = cart_collection.find_one({"user_id": user_id})
        if not cart:
            cart = {"user_id": user_id, "items": [], "total_price": 0}
            cart_collection.insert_one(cart)

        product_ids_in_cart = set()
        cart["items"] = []
        for product in request_body:
            product_id = product.get("product_id")
            product_name = product.get("product_name")
            price = product.get("price")
            seller_email = product.get("seller_email")
            quantity = product.get("quantity")
            image_url = product.get("image_url")
            if product_id not in product_ids_in_cart and quantity > 0:
                cart["items"].append(
                    {
                        "product_id": product_id,
                        "product_name": product_name,
                        "price": price,
                        "seller_email": seller_email,
                        "quantity": quantity,
                        "image_url": image_url,
                    }
                )

        cart["total_price"] = calculate_cart_total(cart["items"])

        cart_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "items": cart["items"],
                    "total_price": round(cart["total_price"], 2),
                }
            },
        )
        del cart["_id"]

        return jsonify({"code": 200, "data": cart}), 200
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/cart/clear/<string:user_id>", methods=["PUT"])
def clear_cart_by_user_id(user_id):
    try:
        cart = cart_collection.find_one({"user_id": user_id})
        if not cart:
            cart = {"user_id": user_id, "items": [], "total_price": 0}
            cart_collection.insert_one(cart)
            del cart["_id"]
            return jsonify({"code": 200, "data": cart}), 200

        cart["items"] = []
        cart["total_price"] = 0

        cart_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "items": cart["items"],
                    "total_price": round(cart["total_price"], 2),
                }
            },
        )
        del cart["_id"]

        return jsonify({"code": 200, "data": cart}), 200
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
