import bcrypt
import json
import os
import datetime
import jwt
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
mongo_client = MongoClient(URI)
db = mongo_client["customers"]
collection = db["customers_details"]
kong_admin_url = "http://host.docker.internal:8001"

# Load the secret key from the JSON file
with open(os.path.join(os.path.dirname(__file__), "secret.json")) as f:
    secret = json.load(f)["secret"]

def hash_password(password_bytes, salt):
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify(
        username=secret
    ), 200


@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    salt = bcrypt.gensalt()
    data["salt"] = salt

    password_bytes = (data.get("password") + secret).encode("utf-8")
    data["password"] = hash_password(password_bytes, salt)
    user = collection.find_one({"email": data.get("email")})
    if user:
        return {"message": "User has already been registered." }, 400
    else:
        # call kong to create new consumer
        result = invoke_http(kong_admin_url + "/consumers", json={"username":data.get("email")}, method="POST")
        data["uuid"] = result.get("id")
        collection.insert_one(data)
        return {"message": "Registration successful."}, 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    result = collection.find_one({"email": data.get("email")})
    if not result:
        return {"message": "User not found."}, 400

    print(data.get("password"))
    print(secret)

    password_bytes = (data.get("password") + secret).encode("utf-8")
    data["password"] = hash_password(password_bytes, result["salt"])
    
    if result["password"] == data.get("password"):
        # call konga to create credentials / issue jwt token
        revoke_all(result.get("uuid"))
        result = invoke_http(kong_admin_url + "/consumers/" + result.get("uuid") + "/jwt", method="POST")

        payload_data = {
            "email": data.get("email"),
            "exp": str(datetime.datetime.now() + datetime.timedelta(seconds=200000000))
        }

        token = jwt.encode(payload=payload_data, key=result["secret"], algorithm="HS256", headers={"iss": result["key"]})
        return {"message": "Login successful", "bearer_token": token}, 200
    else:
        return {"message": "Invalid credentials"}, 401

@app.route("/logout", methods=["POST"])
def logout():
    result = invoke_http(kong_admin_url + "/consumers", json={"username": "john"}, method="POST")
    return result

def revoke_all(consumer_id):
    jwt_url = kong_admin_url + "/consumers/" + consumer_id + "/jwt"
    jwts = invoke_http(jwt_url, method="GET")
    if(len(jwts["data"]) != 0):
        for jwt in jwts["data"]:
            _ = invoke_http(jwt_url + "/" + jwt["id"], method="DELETE")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
