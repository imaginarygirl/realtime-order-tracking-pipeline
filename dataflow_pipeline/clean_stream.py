import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import json
from google.auth import default
from datetime import datetime, timezone

class ParseMessage(beam.DoFn):
    def process(self, element):
        print("📦 RAW ELEMENT:", element)
        message = json.loads(element.decode("utf-8"))
        message["event_timestamp"] = datetime.now(timezone.utc).isoformat()
        print("✅ PARSED MESSAGE:", message)
        yield message

def run():
    project_id = "realtime-order-track-pipeline"
    topic = f"projects/{project_id}/topics/clean-orders-topic"
    dataset_id = "order_tracking"
    table_id = "clean_order_status_stream"
    region = "europe-west1"

    options = PipelineOptions(
        streaming=True,
        project=project_id,
        region=region,
        temp_location=f"gs://{project_id}-dataflow/tmp",
        save_main_session=True,
    )
    options.view_as(StandardOptions).runner = "DataflowRunner"

    with beam.Pipeline(options=options) as p:
        (p
         | "ReadFromPubSub" >> beam.io.ReadFromPubSub(topic=topic).with_output_types(bytes)
         | "ParseMessage" >> beam.ParDo(ParseMessage())
         | "WriteToBQ" >> beam.io.WriteToBigQuery(
             table=f"{project_id}:{dataset_id}.{table_id}",
             schema="order_id:STRING,status:STRING,timestamp:STRING,event_timestamp:TIMESTAMP",
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
         )
        )

if __name__ == "__main__":
    run()
