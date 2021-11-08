
import logging
from google.cloud import bigquery

def load_json(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    filename = event['name']
    bucket = event['bucket']
    uri = "gs://{}/{}".format(bucket, filename)
    table_id = 'analise.my_table'

    # Setting up BigQuery job
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
      source_format='NEWLINE_DELIMITED_JSON',
      write_disposition = 'WRITE_TRUNCATE'
    )

    # Run load job
    try:
        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
        print("Succesfully loaded file {} to table {}. Job ID = {}".format(filename, table_id, load_job.job_id))

    except Exception as e:
        logging.error('Failed to create load job: %s' % (e))