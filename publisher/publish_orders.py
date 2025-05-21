from google.cloud import pubsub_v1
from google.auth import default
import json
import time
import random
from datetime import datetime, timezone

credentials, _ = default()
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path("realtime-order-track-pipeline", "debug-topic")

ORDER_STATUSES = ['created', 'packed', 'shipped', 'delivered']
ORDER_IDS = [f'ORD-{i:04}' for i in range(1, 11)]

def generate_event():
    order_id = random.choice(ORDER_IDS)
    status = random.choice(ORDER_STATUSES)
    event = {
        "order_id": order_id,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return json.dumps(event).encode("utf-8")

if __name__ == "__main__":
    print("Publishing to:", topic_path)
    while True:
        message = generate_event()
        future = publisher.publish(topic_path, message)
        print("Published:", message)
        time.sleep(2)
