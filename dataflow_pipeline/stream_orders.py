import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import json
import argparse
from datetime import datetime, timezone

class ParseOrderEvent(beam.DoFn):
    def process(self, element):
        try:
            print("RAW ELEMENT:", element)

            message = json.loads(element.decode("utf-8"))
            message["event_timestamp"] = datetime.now(timezone.utc).isoformat()

            print("PARSED MESSAGE:", message)
            yield message

        except Exception as e:
            print("ERROR PARSING ELEMENT:", element)
            print("Exception:", str(e))


def run(project_id, topic, dataset_id, table_id, region):
    options = PipelineOptions(
        streaming=True,
        project=project_id,
        region=region,
        job_name='order-status-stream',
        temp_location=f'gs://{project_id}-dataflow/tmp',
        save_main_session=True,
    )
    options.view_as(StandardOptions).runner = 'DataflowRunner'

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=topic)
            | "Parse JSON" >> beam.ParDo(ParseOrderEvent())
            | "Log Messages" >> beam.Map(print)
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                table=f"{project_id}:{dataset_id}.{table_id}",
                schema='order_id:STRING,status:STRING,timestamp:STRING,event_timestamp:TIMESTAMP',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument('--topic', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--table', required=True)
    parser.add_argument('--region', required=True)
    args, pipeline_args = parser.parse_known_args()

    run(
        project_id=args.project,
        topic=args.topic,
        dataset_id=args.dataset,
        table_id=args.table,
        region=args.region
    )
