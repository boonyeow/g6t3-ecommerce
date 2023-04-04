from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_cors import CORS

# DB Configuration
URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_db_connection = MongoClient(URI)
product_database = mongo_db_connection["product"]
product_collection = product_database["product_details"]

# Flask Configuration
app = Flask(__name__)
CORS(app)


@app.route("/product/get")
def get_all():
    try:
        products = product_collection.find()
        result = []

        for product in products:
            del product["_id"]
            if product:
                result.append(product)

        if not result:
            return jsonify({"code": 404, "message": "No products found."}), 404

        return jsonify({"code": 200, "data": result}), 200

    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/product/seller/<string:seller_email>")
def get_product_by_seller(seller_email):
    try:
        products = product_collection.find({"seller_email": seller_email})
        if not products:
            return jsonify({"code": 404, "message": "No products found."}), 404

        result = []
        for product in products:
            del product["_id"]
            if product:
                result.append(product)

        return jsonify({"code": 200, "data": result}), 200

    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/product/get/<string:product_id>")
def get_product_by_id(product_id):
    try:
        product = product_collection.find_one({"product_id": product_id})
        if not product:
            return jsonify({"code": 404, "message": "Product not found."}), 404

        del product["_id"]

        return jsonify({"code": 200, "data": product}), 200

    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/product/get_by_ids")
def get_products_by_ids():
    try:
        if not request.is_json:
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "Incorrect JSON request body."
                        + str(request.get_data()),
                    }
                ),
                400,
            )

        request_body = request.get_json()

        if not request_body.get("products"):
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "Incorrect JSON request body. 'products' is required"
                        + str(request_body),
                    }
                ),
                400,
            )

        product_ids = request_body.get("products")
        products = product_collection.find({"product_id": {"$in": product_ids}})
        result = []
        for product in products:
            del product["_id"]
            result.append(product)

        return jsonify({"code": 200, "data": result}), 200

    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/product/create", methods=["POST"])
def create_product():
    try:
        if request.is_json:
            product_request = request.get_json()
            if (
                not product_request.get("product_name")
                or not product_request.get("price")
                or not product_request.get("seller")
                or not product_request.get("seller_email")
                or not product_request.get("image_url")
            ):
                return (
                    {
                        "code": 400,
                        "message": "Incorrect JSON request body provided."
                        + str(product_request),
                    }
                ), 400

            new_product = {
                "product_id": "P" + str(product_collection.count_documents({}) + 1),
                "product_name": product_request.get("product_name"),
                "price": float(product_request.get("price")),
                "stock": 0
                if not product_request.get("stock")
                else int(product_request.get("stock")),
                "seller": product_request.get("seller"),
                "seller_email": product_request.get("seller_email"),
                "image_url": product_request.get("image_url"),
            }

            product_collection.insert_one(new_product)
            del new_product["_id"]

            return jsonify({"code": 200, "data": new_product}), 200

        return (
            jsonify(
                {
                    "code": 400,
                    "message": "Invalid JSON request body: " + str(request.get_data()),
                }
            ),
            400,
        )

    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/product/<string:product_id>/<int:stock>", methods=["PUT"])
def update_stock(product_id, stock):
    try:
        product_collection.update_one(
            {"product_id": product_id}, {"$set": {"stock": stock}}
        )

        return jsonify({"code": 200, "message": "Successfully updated"}), 200
    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/product/subtract_stock", methods=["PUT"])
def subtract_stock():
    try:
        if not request.is_json:
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "Invalid JSON request body: "
                        + str(request.get_data()),
                    }
                ),
                400,
            )

        products_to_update = request.get_json()["products"]
        for product in products_to_update:
            quantity, product_id = product.get("quantity"), product.get("product_id")
            product_collection.update_one(
                {"product_id": product_id}, {"$inc": {"stock": -quantity}}
            )

        return jsonify({"code": 200, "message": "Successfully updated"}), 200
    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/product/<string:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        ## Stupid fix for deleting products
        product_collection.delete_one({"product_id": product_id})
        product_collection.insert_one({})

        return jsonify({"code": 200, "message": "Successfully deleted."}), 200
    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5400, debug=True)
