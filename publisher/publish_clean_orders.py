from google.cloud import pubsub_v1
from google.auth import default
import json
import random
import time
from datetime import datetime, timezone

credentials, _ = default()
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path("realtime-order-track-pipeline", "clean-orders-topic")

ORDER_STATUSES = ['created', 'packed', 'shipped', 'delivered']
ORDER_IDS = [f"ORD-{i:04d}" for i in range(1, 101)]  # 100 order IDs

def generate_event():
    order_id = random.choice(ORDER_IDS)
    status = random.choice(ORDER_STATUSES)
    return json.dumps({
        "order_id": order_id,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }).encode("utf-8")

print("🚀 Publishing multiple order events...")
for _ in range(100):  # Adjust to send 100 messages
    data = generate_event()
    future = publisher.publish(topic_path, data)
    print("Published:", future.result())
    time.sleep(0.1)  # Small pause to simulate streaming
