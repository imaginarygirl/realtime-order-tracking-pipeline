import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam import pvalue
import json
import logging
from datetime import datetime, timezone
from google.auth import default

# Setup logging
logging.basicConfig(level=logging.INFO)

class ParseMessage(beam.DoFn):
    def process(self, element):
        try:
            # Decode and parse JSON message
            message = json.loads(element.decode("utf-8"))
            message["event_timestamp"] = datetime.now(timezone.utc).isoformat()
            logging.info(f"Parsed message: {message}")
            yield message
        except Exception as e:
            logging.error(f"Error parsing element: {e}")
            yield pvalue.TaggedOutput('failed', element)

def run():
    # Configuration
    project_id = "realtime-order-track-pipeline"
    topic = f"projects/{project_id}/topics/clean-orders-topic"
    dataset_id = "order_tracking"
    table_id = "clean_order_status_stream"
    region = "europe-west1"

    # Pipeline options
    options = PipelineOptions(
        streaming=True,
        project=project_id,
        region=region,
        temp_location=f"gs://{project_id}-dataflow/tmp",
        save_main_session=True,
        job_name='clean-order-pipeline'
    )
    options.view_as(StandardOptions).runner = "DataflowRunner"

    logging.info("Starting Dataflow pipeline...")

    with beam.Pipeline(options=options) as p:
        parsed = (p
            | "ReadFromPubSub" >> beam.io.ReadFromPubSub(topic=topic).with_output_types(bytes)
            | "ParseMessage" >> beam.ParDo(ParseMessage()).with_outputs('failed', main='parsed')
        )

        # Write successful parses to BigQuery
        parsed['parsed'] | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
            table=f"{project_id}:{dataset_id}.{table_id}",
            schema="order_id:STRING,status:STRING,timestamp:STRING,event_timestamp:TIMESTAMP",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )

        # Log failed messages for future alerting
        parsed['failed'] | "LogFailures" >> beam.Map(lambda x: logging.error(f"Failed message: {x}"))

if __name__ == "__main__":
    run()
