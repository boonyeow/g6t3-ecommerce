from pymongo import MongoClient


URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_db_connection = MongoClient(URI)


# Database name (DB icon inside the MongoDB Compass GUI)
my_database = mongo_db_connection["Carts"]

# Collection/Table name (Folder icon inside the MongoDB Compass GUI)
my_collection = my_database["Carts"]

# Writing into the DB

# Inserting many inside the table
# my_collection.insert_many(
#     [
#     {
#         "product_id": ["P1"],
#         "user_id": "U1",
#         "Quantity": [1],
#         "Amount": [3],
#         "Total Amount": [3],
#     }
#     ]
# )
cartlist = [
    {"cart_id": "1",
     "userId":"U1",
    "products": {"product_id":["P1"],"product_name":["Water Bottle"],"price":[2],"quantity":[2]} 
     
     },
    {"cart_id": "1",
     "userId":"U2",
    "products": {"product_id":["P1","P2"],"product_name":["Water Bottle","Pencil Case"],"price":[2,3],"quantity":[2,4]}
     
     },


]
#to create a new column in the db "total amount" and use productPrice and quantity to auto calculate it

for cart in cartlist:
    # Zip function is used to loop over the price and quantity for each product in the cart
    cartlistZip = zip(cart["products"]["price"], cart["products"]["quantity"])
    # Calculate the total amount by multiplying the price and quantity and adding it to the sum
    cart["totalAmount"] = sum([price * quantity for price, quantity in cartlistZip])

#to create a new column in the db "total amount" and use productPrice and quantity to auto calculate it
# for cart in cartlist:
#     #zip function is to match each key to value
#     cartlistZip = zip(cart["productPrice"], cart["quantity"])
#     #to get the total amt
#     cart["totalAmount"] = sum([price * quantity for price, quantity in cartlistZip])
    
# { "name": "Hannah", "address": "Mountain 21"},
# { "name": "Michael", "address": "Valley 345"},
# { "name": "Sandy", "address": "Ocean blvd 2"},
# { "name": "Betty", "address": "Green Grass 1"},
# { "name": "Richard", "address": "Sky st 331"},
# { "name": "Susan", "address": "One way 98"},
# { "name": "Vicky", "address": "Yellow Garden 2"},
# { "name": "Ben", "address": "Park Lane 38"},
# { "name": "William", "address": "Central st 954"},
# { "name": "Chuck", "address": "Main Road 989"},
# { "name": "Viola", "address": "Sideway 1633"}

my_collection.insert_many(cartlist)
mongo_db_connection.close()
