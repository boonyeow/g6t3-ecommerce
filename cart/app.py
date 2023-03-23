from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from flask_cors import CORS
import os
import uuid


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
    for doc in allCart:
        #stringfy the objectid to use as each unique cartid
        doc['_id'] = str(doc['_id']) 
        cartdata.append(doc)
    if cartdata:

        return jsonify(
            {
            "code":200,
            "data": {
                    "carts": cartdata
                    }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no such cart."
        }
    ), 404

#get the cart of the user
@app.route('/cart/<string:userId>', methods=(['GET']))
def get_user_cart(userId):
    myquery = {"userId": userId}
    carts = my_collection.find(myquery)
    cartdata = []
    for cart in carts:
        #stringfy the objectid to use as each unique cartid
        cart['_id'] = str(cart['_id']) 
        cartdata.append(cart)
    if cartdata:
        return jsonify(
            {
                "code":200,
                "data": {
                    "carts": cartdata
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no such cart."
        }
    ), 404

#create cart func, where i first check if the user has an existing cart, if have, it will return"cart existed", if not, it will create a new cart
#and retrieve the productid and productprice from the productdb and insert into a new cart obj
@app.route("/cart", methods=['POST'])
def create_cart():
    #uuid is random string for a unique cartid
    cart_id = str(uuid.uuid4())[:16]
    data = request.get_json()
    userId = data.get('userId')
    myquery = {"userId": userId}
    cart = my_collection.find(myquery)
    product_id = data['products']['product_id']
    query_list = []
    for x in cart: 
        y = json.loads(json_util.dumps(x))
        query_list.append(y)

    if len(query_list) > 0:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userId": userId
                },
                "message": "Cart already exists for this user."
            }
        ), 400
    
    else:
        # mypdquery = {"product_id": product_id}
        # product_cursor = my_collection.find_one(mypdquery)
        # product_cursor = products_collection.find_one({'product_id': product_id})
        
# Retrieve product information from the "products" collection
        product_query = {"product_id": {"$in": product_id}}
        product_cursor = products_collection.find(product_query)
        products = []
        for product in product_cursor:
            products.append(product)

        # Calculate the total amount for the cart
        total_amount = 0
        for i in range(len(product_id)):
            for product in products:
                if data['products']['product_id'][i] == product["product_id"]:
                    total_amount = total_amount + data['products']['quantity'][i] * product["price"]
                    total_amount = round(total_amount,2)
                # global productPrice
                # productPrice= [product["price"] for product in products]
                
        product_id = product_id
        quantity= data['products']['quantity']
        
        # Create a new cart object and insert it into the database
        cart_object = {
            "cart_id":str(cart_id),
            "userId":userId,
            "products": {"product_id":product_id,"product_name":[product["product_name"] for product in products],"price":[product["price"] for product in products],"quantity":quantity},
            # "price": [product["price"] for product in products],
            "totalAmount": total_amount,
            # "timestamp": datetime.now()
        }
        my_collection.insert_one(cart_object)

        # Return the newly created cart object
        # cart_object["_id"] = str(cart_object["_id"])
        return jsonify(
            {
                "code":200,
                "data": {
                    "carts": cart_object
                },
                "message": "Cart created successfully and product(s) are added."
            }
        )


# @app.route("/cart", methods=['POST'])
# def create_cart():
#     data = request.get_json()
#     user_id = data.get('userId')
#     product_id = data.get('productId')
#     quantity = data.get('quantity')

#     # Query the products collection to get the product price and ID
#     product = my_products_collection.find_one({'product_id': product_id})
#     if not product:
#         return jsonify({
#             'code': 404,
#             'message': 'Product not found',
#         })

#     product_price = product.get('price')
#     total_amount = quantity * product_price

#     existing_cart = my_collection.find_one({'user_id': user_id})
#     if existing_cart:
#         cart_id = existing_cart['_id']
#         existing_cart_items = existing_cart.get('items', [])
#         if not existing_cart_items:
#             return jsonify({
#                 'code': 200,
#                 'message': 'You have nothing in your cart',
#             })
#         for item in existing_cart_items:
#             if item['productId'] == product_id:
#                 # Product already exists in cart, update quantity and total_amount
#                 item['quantity'] += quantity
#                 item['totalAmount'] += total_amount
#                 my_collection.update_one({'_id': cart_id}, {'$set': {'items': existing_cart_items}})
#                 return jsonify({
#                     'code': 200,
#                     'message': 'Cart updated successfully',
#                     'cart_id': str(cart_id),
#                 })
#         # Product not found in cart, add new item
#         new_item = {
#             'productId': product_id,
#             'quantity': quantity,
#             'productPrice': product_price,
#             'totalAmount': total_amount,
#         }
#         existing_cart_items.append(new_item)
#         my_collection.update_one({'_id': cart_id}, {'$set': {'items': existing_cart_items}})
#         return jsonify({
#             'code': 200,
#             'message': 'Cart updated successfully',
#             'cart_id': str(cart_id),
#         })
#     else:
#         # Create new cart
#         new_cart = {
#             'user_id': user_id,
#             'items': {
#                 'productId': [product_id],
#                 'quantity': [quantity],
#                 'productPrice': [product_price],
#                 'totalAmount': total_amount,
#             },
#         }
#         result = my_collection.insert_one(new_cart)
#         return jsonify({
#             'code': 201,
#             'message': 'Cart created successfully',
#             'cart_id': str(result.inserted_id),
#         })


# @app.route("/cart/<string:userid>", methods=['POST'])
# def create_order(userid):
#     myquery = {"userId": userid}
#     cart = my_collection.find(myquery)
#     query_list = []
#     for x in cart: 
#         y = json.loads(json_util.dumps(x))
#         query_list.append(y)

#     if len(query_list) >0:
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "userId":userid
#                 },
#                 "message": "Cart already exists."
#             }
#         ), 400
    
#     else:
#         data = request.get_json()
#         my_collection.insert_one(
#             {
#                 "_id": data["_id"],
#                 "user_id": data["user_id"],
#                 "product_id": data["product_id"],
#                 "quantity":data["quantity"],
#                 "productPrice":data["productPrice"],
#                 "totalamount":data["totalAmount"]
#             }
#         )
#         #order created successfully
#         return jsonify({
#             "code": "201",
#             "data": data
#         }), 201

    #need except for if cart not created successfully
# @app.route('/cart/<string:cartId>"', methods=('GET', 'POST'))
# def getall():
#     allCart = my_collection.find_one({cartId})
#     return jsonify({
#         "code":200
#     })

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
if __name__ == '__main__':
    app.run(port=5000, debug=True, host='localhost', threaded=True)