from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe

# Config
stripe.api_key = "sk_test_51MmY6dHbLz6qKWZ5irldB118SLEuzKha9E14crPg6Wpn18F6lfBiLb8OfxWTSjs5QziQC21tZF0EClvONpSvtdQY00XYkANuA9"
app = Flask(__name__, static_url_path="", static_folder="public")
CORS(app)


@app.route("/payment/check_card_validity")
def check_card_validity():
    try:
        if not request.is_json:
            return jsonify({"code": 400, "message": "Invalid JSON request"})
        request_body = request.get_json()

        customer = stripe.Customer.create(email=request_body["customer_email"])
        stripe_token = stripe.Token.create(card=request_body["card"])
        stripe.Customer.create_source(customer["id"], source=stripe_token)
        print(stripe_token)

        return jsonify({"code": 200, "data": "card valid"}), 200
    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/payment/make_payment", methods=["POST"])
def make_payment():
    try:
        if not request.is_json:
            return jsonify({"code": 400, "message": "Invalid JSON request"})

        request_body = request.get_json()
        stripe_token = stripe.Token.create(card=request_body["card"])["id"]
        payment_amount = request_body["payment_amount"]

        stripe_charge = stripe.Charge.create(
            amount=payment_amount, currency="sgd", source=stripe_token
        )
        print(stripe_charge)

        return jsonify({"code": 200, "message": "Successful payment!"})
    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


if __name__ == "__main__":
    print("Go to the url below for test card numbers")
    print("https://stripe.com/docs/testing#cards")
    app.run(host="0.0.0.0", port=5700, debug=True)
