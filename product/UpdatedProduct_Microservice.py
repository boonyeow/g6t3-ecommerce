from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)

URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_db_connection = MongoClient(URI)
my_database = mongo_db_connection["product"]
my_collection = my_database["product_details"]

def json_converter(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

@app.route('/products')
def getAll():
    try:
        products = my_collection.find()
        product_list = list(products)

        if product_list:
            return jsonify(
                {
                    "code": 200,
                    "data": json.dumps(product_list, default=json_converter)
                }
            )
        else:
            return jsonify(
                {
                    "code": 200,
                    "data": []
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Internal server error: {}".format(str(e))
            }
        ), 500
    
@app.route('/products/<string:productid>')
def getProduct(productid):
    try:
        myquery = {"product_id": productid}
        product_result = my_collection.find(myquery)
        product_list = list(product_result)

        if product_list:
            return jsonify(
                {
                    "code": 200,
                    "data": json.dumps(product_list, default=json_converter)
                }
            )
        else:
            return jsonify(
                {
                    "code": 200,
                    "data": []
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Internal server error: {}".format(str(e))
            }
        ), 500    

######################################################################
@app.route('/products/<string:productid>/stock')
def UpdateProductStock(productid,quantity=3):     ##I am hard coding the quantity here just for testing, by right quantity should be a derived field
                                                  #should change quantity = 3 to quantity              
    try:
        myquery = {"product_id": productid}
        product_result = my_collection.find(myquery)
        
        product_list = list(product_result)
        #print(product_list[0]['stock'])
        product_stock = product_list[0]['stock']
        updated_stock = product_stock - quantity
        update={'$set': {'stock': updated_stock}}
        #print(updated_stock)
        if updated_stock:
            my_collection.update_one(myquery,update)  ##currently I am only returning the stock number but actually idt need to return anything
            return jsonify(
                {
                    "code": 200,
                    "data": json.dumps(updated_stock, default=json_converter)
                }
            )
        else:
            return jsonify(
                {
                    "code": 200,
                    "data": []
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Internal server error: {}".format(str(e))
            }
        ), 500    

if __name__ == '__main__':
    app.run(port=5000, debug=True)