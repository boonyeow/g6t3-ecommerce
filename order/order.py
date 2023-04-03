import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

# DB Configuration
URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_db_connection = MongoClient(URI)
order_database = mongo_db_connection["order"]
order_collection = order_database["order_details"]

# Flask Configuration
app = Flask(__name__)
CORS(app)


# get all orders from collection - order_details
@app.route("/order/get")
def get_all():
    try:
        all_orders = order_collection.find()
        result = []
        for order in all_orders:
            del order["_id"]
            if order:
                result.append(order)

        if not result:
            return jsonify({"code": 404, "message": "No orders found."}), 404

        return jsonify({"code": 200, "data": result}), 200

    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


# retrieve order by order id
@app.route("/order/get/<string:order_id>")
def find_by_order_id(order_id):
    try:
        order = order_collection.find_one({"order_id": order_id})
        if not order:
            return jsonify({"code": 404, "message": "Order not found."}), 404

        del order["_id"]

        return jsonify({"code": 200, "data": order}), 200

    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/order/get/user/<string:user_id>")
def find_by_user_id(user_id):
    try:
        orders = order_collection.find({"user_id": user_id})
        if not orders:
            return jsonify({"code": 404, "message": "Order not found."}), 404

        result = []
        for order in orders:
            del order["_id"]
            if order:
                result.append(order)

        return jsonify({"code": 200, "data": result}), 200
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/order/create", methods=["POST"])
def create_new_order():
    try:
        if request.is_json:
            order_request = request.get_json()
            if not order_request.get("items") or not order_request.get("user_id"):
                return jsonify(
                    {
                        "code": 400,
                        "message": "Incorrect JSON request body provided."
                        + str(request.get_json()),
                    }
                )

            new_order = {
                "order_id": "O" + str(order_collection.count_documents({}) + 1),
                "items": [item for item in order_request.get("items")],
                "user_id": order_request.get("user_id"),
                "time": datetime.datetime.utcnow(),
                "status": "Pending",
            }
            order_collection.insert_one(new_order)
            del new_order["_id"]

            return jsonify({"code": 200, "data": new_order}), 200

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
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/order/complete/<string:order_id>", methods=["PUT"])
def complete_order_payment(order_id):
    try:
        order = order_collection.find_one({"order_id": order_id})
        if not order:
            return jsonify({"code": 404, "message": "Order not found."})

        paid_amount = 0
        for item in order["items"]:
            paid_amount += item["price"] * item["quantity"]

        order["paid_amount"] = round(paid_amount, 2)
        order["status"] = "Processing"

        order_collection.update_one(
            {"order_id": order_id},
            {"$set": {"status": order["status"], "paid_amount": order["paid_amount"]}},
        )

        del order["_id"]

        return (
            jsonify({"code": 200, "message": "Successfully updated.", "data": order}),
            200,
        )
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/order/failed/<string:order_id>", methods=["PUT"])
def failed_order(order_id):
    try:
        order = order_collection.find_one({"order_id": order_id})
        if not order:
            return jsonify({"code": 404, "message": "Order not found."})

        order["paid_amount"] = 0.00
        order["status"] = "Failed"

        order_collection.update_one(
            {"order_id": order_id},
            {"$set": {"status": order["status"], "paid_amount": order["paid_amount"]}},
        )

        del order["_id"]

        return (
            jsonify({"code": 200, "data": order, "message": "Successfully updated."}),
            200,
        )
    except Exception as e:
        return (
            jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5300, debug=True)
