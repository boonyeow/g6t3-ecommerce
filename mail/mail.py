#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
import requests
import os
import sys
import json
import amqp_setup


routing_key = "*.mail"

MAILGUN_API_KEY = "2e180d571da57a8248b82a70678ed950-30344472-13c94507"
MAILGUN_DOMAIN_NAME = "sandbox061f45162bc1421eaa4af62f3b6446ae.mailgun.org"
FRONTEND_URL = "http://localhost:3000"


def receive_mail():
    queue_name = "mail"
    amqp_setup.check_setup()
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True
    )
    amqp_setup.channel.start_consuming()


def callback(channel, method, properties, body):
    print("\nReceived a mail request by " + __file__)
    result = send_email(body)
    log_process(result)
    print("\n\nEnd callback process\n\n")


def send_email(body):
    try:
        incoming_data = json.loads(body)
    except Exception as e:
        print("Failed to decode JSON")
        return {"code": 400, "message": "Invalid JSON input: " + body}

    print(f"Received: {incoming_data}")

    try:
        recipient = incoming_data["recipient"]
        if incoming_data["type"] == "bad_review":
            product_name = incoming_data["product_name"]
            product_id = incoming_data["product_id"]
            reviewer_id = incoming_data["user_id"]
            review_description = incoming_data["review_description"]
            review_stars = incoming_data["review_stars"]
            result = send_mail(
                recipient,
                f"Bad review ({review_stars} star) received on {product_name} by {reviewer_id}",
                f"""
                Hello,<br/><br/>
                A user ({reviewer_id}) has just left an unsatisfactory review for your product ({FRONTEND_URL}/product/{product_id})<br/><br/>
                This is the message left by the user: <b>{review_description}</b><br/><br/>
                You may want to follow up with them for further details.<br/>
                Thank you for choosing ESD G6T3 as your e-commerce platform!<br/><br/>
                Regards,<br/>
                ESD G6T3
                """,
            )
        elif incoming_data["type"] == "order_processing":
            order = incoming_data["order"]
            
            subject=""
            message=""
            result=send_email(recipient, subject, message)

        if result["code"] == 200:
            print(f"Message succesfully sent to {recipient}")
        else:
            print(f"Failed to send message{result}")
        return result
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        exception_str = f"{str(e)} at {exc_type}: {fname} : line {exc_tb.tb_lineno}"
        print(exception_str)
        return {"code": 500, "message": fname + " error: " + exception_str}


def send_mail(recipient, subject, message):
    try:
        r = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"ESD G6T3 <esd-g6t3@{MAILGUN_DOMAIN_NAME}>",
                "to": [recipient],
                "subject": subject,
                "text": message,
                "html": message,
            },
        )
        if r.status_code == 200:
            return {"code": r.status_code, "message": "Successfully sent mail"}
        print(r)
        return {"code": 500, "message": "Failed to send mail."}
    except Exception as e:
        return {"code": 500, "message": "Failed to send mail."}


def log_process(result):
    print("\n\nMail message:")
    try:
        print("JSON--:", str(result))
        print(result)
    except Exception as e:
        print("Exception:", e)
        print("Data:", result)
        print()


if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__))
    print(
        f"Monitoring routing key: '{routing_key}' in exchange: '{amqp_setup.exchangename}'"
    )
    receive_mail()
