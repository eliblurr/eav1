# handle stripe payment intents here
#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
import json
import os
import stripe
stripe.api_key = os.environ.get('STRIPE_API_KEY') or "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

# from flask import Flask, render_template, jsonify, request


# app = Flask(__name__, static_folder=".",
#             static_url_path="", template_folder=".")




# @app.route('/create-payment-intent', methods=['POST'])
def create_payment(order_amount:float):
    try:
        # data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=order_amount,
            currency='usd'
        )

        print(intent)

        # return jsonify({
        #   'clientSecret': intent['client_secret']
        # })
    except Exception as e:
        return jsonify(error=str(e)), 403

async def payout():
    return

# if __name__ == '__main__':
#     app.run()