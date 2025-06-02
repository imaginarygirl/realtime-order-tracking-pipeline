import os
import requests
from google.cloud import pubsub_v1
from flask import Flask

app = Flask(__name__)

# Finnhub API setup
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY")
FINNHUB_SYMBOL = os.environ.get("FINNHUB_SYMBOL", "AAPL")  # Default to AAPL

# Pub/Sub setup
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.route("/")
def ingest_data():
    url = f"https://finnhub.io/api/v1/quote?symbol={FINNHUB_SYMBOL}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        message = {
            "symbol": FINNHUB_SYMBOL,
            "current_price": data["c"],
            "high_price": data["h"],
            "low_price": data["l"],
            "open_price": data["o"],
            "previous_close": data["pc"],
            "timestamp": data["t"]
        }
        message_bytes = str(message).encode("utf-8")
        publisher.publish(topic_path, message_bytes)
        return f"Published: {message}"
    else:
        return f"Error fetching data: {response.status_code}"

if __name__ == "__main__":
    app.run(debug=True)
