from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_cors import CORS

# DB Configuration
URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_db_connection = MongoClient(URI)
product_notification_database = mongo_db_connection["product_notification"]
product_notification_collection = product_notification_database[
    "product_notification_details"
]

# Flask Configuration
app = Flask(__name__)
CORS(app)


@app.route("/product_notification/get/<string:product_id>")
def get_users_in_notification_list(product_id):
    try:
        product_notification = product_notification_collection.find_one(
            {"product_id": product_id}
        )

        if not product_notification:
            return jsonify({"code": 200, "data": []}), 200

        return jsonify({"code": 200, "data": product_notification["user_ids"]}), 200

    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route(
    "/product_notification/<string:user_id>/<string:product_id>", methods=["POST"]
)
def add_user_to_product_notification(user_id, product_id):
    try:
        product_notification = product_notification_collection.find_one(
            {"product_id": product_id}
        )
        if not product_notification:
            product_notification_collection.insert_one(
                {"product_id": product_id, "user_ids": [user_id]}
            )
            return jsonify({"code": 200, "message": "Successfully added!"}), 200

        if user_id not in product_notification["user_ids"]:
            product_notification["user_ids"].append(user_id)

            product_notification_collection.update_one(
                {"product_id": product_id},
                {"$set": {"user_ids": product_notification["user_ids"]}},
            )

        return jsonify({"code": 200, "message": "Successfully added!"}), 200
    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route(
    "/product_notification/<string:user_id>/<string:product_id>", methods=["GET"]
)
def check_if_user_already_notified(user_id, product_id):
    try:
        product_notification = product_notification_collection.find_one(
            {"product_id": product_id}
        )
        if not product_notification or user_id not in product_notification["user_ids"]:
            return jsonify({"code": 200, "data": False}), 200

        return jsonify({"code": 200, "data": True}), 200

    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/product_notification/clear/<string:product_id>", methods=["PUT"])
def clear_notification_list(product_id):
    try:
        product_notification = product_notification_collection.find_one(
            {"product_id": product_id}
        )
        if not product_notification:
            return jsonify({"code": 200, "message": "Successfully cleared!"}), 200

        product_notification_collection.update_one(
            {"product_id": product_id}, {"$set": {"user_ids": []}}
        )

        return jsonify({"code": 200, "message": "Successfully cleared!"}), 200

    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800, debug=True)
