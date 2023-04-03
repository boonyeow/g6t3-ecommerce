from flask import Flask, request
from flask_cors import CORS
# from pymongo import MongoClient

import stripe

stripe.api_key = "sk_test_51MmY6dHbLz6qKWZ5irldB118SLEuzKha9E14crPg6Wpn18F6lfBiLb8OfxWTSjs5QziQC21tZF0EClvONpSvtdQY00XYkANuA9"

app = Flask(__name__,
            static_url_path='',
            static_folder='public')
CORS(app)

DOMAIN = 'http://127.0.0.1:5600'

# URI = "mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test"
# mongo_db_connection = MongoClient(URI)


@app.route('/api/checkout', methods=['POST'])
def checkout():
    try:
        request_data = request.get_json()

        line_items = []
        for item in request_data:
            line_items.append({
                'price': item['price'],
                'quantity': item['quantity']
            })

        checkout_session = stripe.checkout.Session.create(
            line_items=request_data,
            mode='payment',
            success_url=DOMAIN + '/success.html',
            cancel_url=DOMAIN + '/cancel.html',
        )
    except Exception as e:
        print("heye", e)
        return str(e)

    return checkout_session.url


if __name__ == '__main__':
    app.run(port=5600, debug=True)
