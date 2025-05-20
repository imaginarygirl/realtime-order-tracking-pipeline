from google.cloud import pubsub_v1
import json
import time
import random
from datetime import datetime, timezone
from google.auth import default


PROJECT_ID = 'realtime-order-track-pipeline'
TOPIC_ID = 'order-status-events'

credentials, _ = default()
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

ORDER_STATUSES = ['created', 'packed', 'shipped', 'delivered']
ORDER_IDS = [f'ORD-{i:04}' for i in range(1, 11)]  # 10 sample orders

def generate_event():
    order_id = random.choice(ORDER_IDS)
    status = random.choice(ORDER_STATUSES)
    event = {
        "order_id": order_id,
        "status": status,
        #"timestamp": datetime.utcnow().isoformat()
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return json.dumps(event).encode("utf-8")

if __name__ == "__main__":
    print("Publishing order events to Pub/Sub...")
    while True:
        message = generate_event()
        future = publisher.publish(topic_path, message)
        print(f"Published: {message}")
        time.sleep(2)  # Adjust frequency as needed
