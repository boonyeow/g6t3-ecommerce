from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from flask_cors import CORS
import os
import uuid
import math


app = Flask(__name__)
CORS(app)

URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_db_connection = MongoClient(URI)

#cart db
my_database = mongo_db_connection["Carts"]
my_collection = my_database["Carts"]

#product db
my_product_database = mongo_db_connection["product"]

products_collection = my_product_database["product_details"]

@app.route('/', methods=('GET', 'POST'))
def index():
    carts = my_collection.find()
    return render_template('cart.html', carts=carts)
    # template_dir = 'C:/wamp64/www/ESDProj'
    # return render_template(os.path.join(template_dir, 'cart.html'))
    # return render_template('index.html')

#get all carts
@app.route('/cart', methods=(['GET']))
def getall():
    allCart = list(my_collection.find({}))
    cartdata = []
    for x in allCart: 
        y = json.loads(json_util.dumps(x))
        cartdata.append(y)
    if cartdata:

        return jsonify(
            {
            "code":200,
            "data": {
                    "carts": [cart for cart in cartdata]
                    }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User does not have a cart."
        }
    ), 404

#get the cart of the user
@app.route('/cart/<string:userId>', methods=(['GET']))
def get_user_cart(userId):
    myquery = {"userId": userId}
    cart = my_collection.find(myquery)
    cartdata = []
    for x in cart: 
        y = json.loads(json_util.dumps(x))
        cartdata.append(y)
    if cartdata:
        return jsonify(
            {
                "code":200,
                "data": {
                    "cart": [cart for cart in cartdata]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User does not have a cart."
        }
    ), 404


#create cart
@app.route("/cart", methods=['POST'])
def create_cart():
    #uuid is random string for a unique cartid
    cart_id = str(uuid.uuid4())[:16]
    data = request.get_json()
    userId = data.get('userId')
    myquery = {"userId": userId}

    cart = my_collection.find(myquery)
    
    query_list = []
    for x in cart: 
        y = json.loads(json_util.dumps(x))
        query_list.append(y)

    if len(query_list) > 0:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userId": [cart for cart in query_list]
                },
                "message": "Cart already exists for this user."
            }
        ), 400
    
    else:
        
        product_id = data['products']['product_id']
        product_name = data['products']['product_name']
        price = data['products']['price']
        quantity = data['products']['quantity']

        # Zip function is used to loop over the price and quantity for each product in the cart
        cartlistZip = zip(price, quantity)

        cart_object = {
            "cart_id":str(cart_id),
            "userId":userId,
            "products": {"product_id":product_id,"product_name":product_name,"price":price,"quantity":quantity}
            # "price": [product["price"] for product in products],
            # "timestamp": datetime.now()
        }
        # Calculate the total amount by multiplying the price and quantity and adding it to the sum
        cart_object["totalAmount"] = round(sum([price * quantity for price, quantity in cartlistZip]),2)
        my_collection.insert_one(cart_object)
        return jsonify({
            "code": "201",
            "data": cart_object,
            "message":"Cart Created successfully"
        }), 201

#update user cart
@app.route('/cart/<string:userId>', methods=['PUT'])
def update_cart(userId):
    data = request.get_json()
    quantity = data.get('products').get('quantity')
    myquery = {'userId': userId}
    cart = my_collection.find_one(myquery)
    price = cart['products']['price']
    query_list = []
    for x in cart: 
        y = json.loads(json_util.dumps(x))
        query_list.append(y)

    if cart is None:
        return jsonify({
            "code": "400",
            "message":"Cart does not exist"
        }), 400
    
    #first update the quantity
    update = {'$set': {'products.quantity': quantity}}
    cart_object = my_collection.update_one(myquery, update)

    #zip the price with qty coz i wan find total
    cartlistZip = zip(price, quantity)
    updatedTotal = round(sum([price * quantity for price, quantity in cartlistZip]),2)

    #second update is the total amount
    update2 = {'$set': {'totalAmount': updatedTotal}}
    cart_object = my_collection.update_one(myquery, update2)

    if cart_object.modified_count == 0:
        return jsonify({
            "code": "400",
            "message":"Product is not in the Cart. Please add product to cart"
        }), 400

    return jsonify({
        "code": "201",
        "message":"Product Quantity has been updated into the cart"
    }), 201


#delete user cart
@app.route('/cart', methods=['DELETE'])
def delete_cart():
    data = request.get_json()
    userId = data.get('userId')
    myquery = {"userId": userId}
    cart = my_collection.find(myquery)
    my_collection.delete_one({ "userId": userId })
    # if cart:
    #     return jsonify(
    #         {
    #             "code":404,
    #             "data": {
    #                 "carts": list(cart),
    #             },
    #             "message":"This user cart cannot be deleted"
    #         }
    #     )
    return jsonify(
        {
            "code": 200,
            "message": "Cart has been successfully deleted."
        }
    ), 404




#create cart func, where i first check if the user has an existing cart, if have, it will return"cart existed", if not, it will create a new cart
#and retrieve the productid and productprice from the productdb and insert into a new cart obj (more for adding to cart complex ms)
# @app.route("/cart", methods=['POST'])
# def create_cart():
#     #uuid is random string for a unique cartid
#     cart_id = str(uuid.uuid4())[:16]
#     data = request.get_json()
#     userId = data.get('userId')
#     myquery = {"userId": userId}

#     cart = my_collection.find(myquery)
    
#     product_id = data['products']['product_id']
#     query_list = []
#     for x in cart: 
#         y = json.loads(json_util.dumps(x))
#         query_list.append(y)

#     if len(query_list) > 0:
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "userId": userId
#                 },
#                 "message": "Cart already exists for this user."
#             }
#         ), 400
    
#     else:
#         # mypdquery = {"product_id": product_id}
#         # product_cursor = my_collection.find_one(mypdquery)
#         # product_cursor = products_collection.find_one({'product_id': product_id})
        
# # Retrieve product information from the "products" collection
#         product_query = {"product_id": {"$in": product_id}}
#         product_cursor = products_collection.find(product_query)
#         products = []
#         for product in product_cursor:
#             products.append(product)

#         # Calculate the total amount for the cart
#         total_amount = 0
#         for i in range(len(product_id)):
#             for product in products:
#                 if data['products']['product_id'][i] == product["product_id"]:
#                     total_amount = total_amount + data['products']['quantity'][i] * product["price"]
#                     total_amount = round(total_amount,2)
#                 # global productPrice
#                 # productPrice= [product["price"] for product in products]
                
#         product_id = product_id
#         quantity= data['products']['quantity']
        
#         # Create a new cart object and insert it into the database
#         cart_object = {
#             "cart_id":str(cart_id),
#             "userId":userId,
#             "products": {"product_id":product_id,"product_name":[product["product_name"] for product in products],"price":[product["price"] for product in products],"quantity":quantity},
#             # "price": [product["price"] for product in products],
#             "totalAmount": total_amount,
#             # "timestamp": datetime.now()
#         }
#         my_collection.insert_one(cart_object)

#         # Return the newly created cart object
#         # cart_object["_id"] = str(cart_object["_id"])
#         return jsonify(
#             {
#                 "code":200,
#                 "data": {
#                     "carts": cart_object
#                 },
#                 "message": "Cart created successfully and product(s) are added."
#             }
#         )



if __name__ == '__main__':
    app.run(port=5000, debug=True, host='localhost', threaded=True)