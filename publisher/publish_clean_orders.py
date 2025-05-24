from google.cloud import pubsub_v1
from google.auth import default
import json
from datetime import datetime, timezone

credentials, _ = default()
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path("realtime-order-track-pipeline", "clean-orders-topic")

data = json.dumps({
    "order_id": "ORD-0001",
    "status": "created",
    "timestamp": datetime.now(timezone.utc).isoformat()
}).encode("utf-8")

future = publisher.publish(topic_path, data)
print("Published:", future.result())
