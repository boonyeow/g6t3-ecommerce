from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
import os

stripe.api_key = "sk_test_51MmY6dHbLz6qKWZ5irldB118SLEuzKha9E14crPg6Wpn18F6lfBiLb8OfxWTSjs5QziQC21tZF0EClvONpSvtdQY00XYkANuA9"

app = Flask(__name__, static_url_path="", static_folder="public")
CORS(app)

DOMAIN = os.environ.get("PAYMENT_URL") or "http://localhost:5700"


@app.route("/payment/checkout", methods=["POST"])
def checkout():
    try:
        # request_data = request.get_json()

        # for item in request_data:
        #     line_items.append({"price": item["price"], "quantity": item["quantity"]})

        # Hardcoded items
        line_items = [
            {"price": "price_1Mna83HbLz6qKWZ5a1QSqny9", "quantity": 123},
            {"price": "price_1Mna6xHbLz6qKWZ5ISjiOzZP", "quantity": 123},
            {"price": "price_1Mna6xHbLz6qKWZ5ISjiOzZP", "quantity": 123},
        ]

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=DOMAIN + "/success.html",
            cancel_url=DOMAIN + "/cancel.html",
        )
        return jsonify({"code": 200, "payment_link": checkout_session.url}), 200
    except Exception as e:
        return (
            jsonify(
                {"code": 500, "message": "Internal server error: {}".format(str(e))}
            ),
            500,
        )


@app.route("/payment/stripe_webhook", methods=["POST"])
def stripe_webhook():
    # https://stripe.com/docs/webhooks
    # https://stripe.com/docs/payments/payment-intents/verifying-status
    payload = request.get_data()
    sig_header = request.headers.get("STRIPE_SIGNATURE")
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # invalid signature
        return "Invalid signature", 400

    event_dict = event.to_dict()
    if event_dict["type"] == "payment_intent.succeeded":
        intent = event_dict["data"]["object"]
        print("Succeeded: ", intent["id"])
        # Fulfill the customer's purchase

    elif event_dict["type"] == "payment_intent.payment_failed":
        intent = event_dict["data"]["object"]
        error_message = (
            intent["last_payment_error"]["message"]
            if intent.get("last_payment_error")
            else None
        )
        print("Failed: ", intent["id"]), error_message
        # Notify the customer that payment failed

    return "OK", 200


if __name__ == "__main__":
    app.run(port=5700, debug=True)
