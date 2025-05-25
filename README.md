```markdown
# 📦 Real-Time Order Tracking Pipeline

This project showcases a **real-time data engineering pipeline** built on **Google Cloud Platform (GCP)**, designed to ingest, process, and visualize order status events.

## 🚀 **Technologies Used**
- **Google Pub/Sub**: For real-time event ingestion  
- **Google Dataflow**: For stream processing and transformation  
- **Google BigQuery**: For scalable storage and analytics  
- **Google Cloud Functions + SendGrid**: For email alerts on failed messages  
- **Looker Studio (Google Data Studio)**: For live dashboards and visualization  

## 🏗️ **Architecture**
```

\[Order Status Events] → \[Pub/Sub] → \[Dataflow] → \[BigQuery]
↘
\[Cloud Functions → Email Alerts]

````

- Orders are ingested via Pub/Sub topics (simulating API ingestion).
- Dataflow processes events, adds timestamps, and writes to BigQuery.
- Cloud Functions trigger on failed messages and send email alerts.
- Looker Studio visualizes data in real-time.

## 📊 **Live Dashboard**
- 🔗 [Looker Studio Dashboard](https://lookerstudio.google.com/s/rlXcx5VnXuA)
- 📄 [Dashboard PDF Mockup](dashboard/dashboard_mockup.pdf)

## 📂 **Setup Instructions**
1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/imaginarygirl/realtime-order-tracking-pipeline.git
cd realtime-order-tracking-pipeline
````

2️⃣ **Set Up GCP Services**

* Enable Pub/Sub, Dataflow, BigQuery, Cloud Functions
* Create Pub/Sub topics and BigQuery datasets

3️⃣ **Deploy the Dataflow Pipeline**

```bash
python dataflow_pipeline/clean_stream.py --project=<GCP_PROJECT_ID> --topic=<PUBSUB_TOPIC> --dataset=<BQ_DATASET> --table=<BQ_TABLE> --region=<GCP_REGION>
```

4️⃣ **Deploy Cloud Function for Alerts**

```bash
cd failed_message_alert
gcloud functions deploy failed-message-email-alert \
  --runtime python311 \
  --trigger-topic failed-messages-topic \
  --set-env-vars SENDGRID_API_KEY=<SENDGRID_API_KEY>,SENDGRID_FROM_EMAIL=<YOUR_EMAIL>,ALERT_TO_EMAIL=<YOUR_EMAIL> \
  --entry-point pubsub_trigger \
  --source=.
```

5️⃣ **Run the Publisher to Simulate Orders**

```bash
python publisher/publish_orders.py
```

## 💬 **Key Features**

✅ Real-time ingestion and processing
✅ Email alerts on message failures
✅ Live dashboards with BigQuery and Looker Studio
✅ Scalable and production-ready architecture

## 📂 **Archive**

Older versions of scripts have been moved to the `archive` folder for reference.

## 🤝 **Connect**

Feel free to reach out and connect with me on [LinkedIn](https://www.linkedin.com/in/camila-martins-532193b0/)!

---
