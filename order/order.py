from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

app = Flask(__name__)

URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_db_connection = MongoClient(URI)
# Database name (DB icon inside the MongoDB Compass GUI)
my_database = mongo_db_connection["order"]

# Collection/Table name (Folder icon inside the MongoDB Compass GUI)
my_collection = my_database["order_details"]

@app.route('/order')
#def index():
 #   return render_template('index.html')

#get all details from collection - order_details
def getAll():

    order = my_collection.find()
    orderlist = []
    for x in order:
        y = json.loads(json_util.dumps(x))
        orderlist.append(y)

    if orderlist:
        return jsonify(
            {
            "code": "200",
            "data": {
                "orders": [ordering for ordering in orderlist]}
        }
        )
        
        #orderlist

    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404

#retrieve order by order id
@app.route("/order/<string:orderid>")
def find_by_orderid(orderid):
    myquery = {"order_id": orderid}
    order = my_collection.find(myquery)
    query_list = []
    for x in order: 
        y = json.loads(json_util.dumps(x))
        query_list.append(y)

    if query_list:
        return jsonify(
            {
                "code": 200,
                "data": [ordering for ordering in query_list]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Order not found."
        }
    ), 404

@app.route("/order/<string:orderid>", methods=['POST'])
def create_order(orderid):
    myquery = {"order_id": orderid}
    order = my_collection.find(myquery)
    query_list = []
    for x in order: 
        y = json.loads(json_util.dumps(x))
        query_list.append(y)

    if len(query_list) >0:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "order_id":orderid
                },
                "message": "Order already exists."
            }
        ), 400
    
    else:
        data = request.get_json()
        my_collection.insert_one(
            {
                "order_id": data["order_id"],
                "product_id": data["product_id"],
                "user_id": data["user_id"]
            }
        )
        #order created successfully
        return jsonify({
            "code": "201",
            "data": data
        }), 201

    #need except for if order not created successfully



if __name__ == '__main__':
    app.run(port=5000, debug=True)