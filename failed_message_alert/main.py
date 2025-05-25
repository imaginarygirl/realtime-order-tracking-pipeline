import base64
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_alert(data):
    message = Mail(
        from_email=os.environ['SENDGRID_FROM_EMAIL'],
        to_emails=os.environ['ALERT_TO_EMAIL'],
        subject='Dataflow Alert: Failed Message Detected',
        plain_text_content=f"Failed message data:\n\n{data}"
    )
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

def pubsub_trigger(event, context):
    if 'data' in event:
        message_data = base64.b64decode(event['data']).decode('utf-8')
        print(f"Received failed message: {message_data}")
        send_email_alert(message_data)
    else:
        print("No data in event")
