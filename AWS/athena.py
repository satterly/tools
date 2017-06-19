#!/usr/local/bin/python

import uuid
import time
import boto3
import json

S3_RESULTS_BUCKET='s3://ophan-query-results'

dbname = 'clean'

query = 'select * from clean.subscriptions limit 10;'

client = boto3.client('athena')

query_execution_id = client.start_query_execution(
    QueryString=query,
    ClientRequestToken=str(uuid.uuid4()),
    QueryExecutionContext={
        'Database': dbname
    },
    ResultConfiguration={
        'OutputLocation': S3_RESULTS_BUCKET
    }
)['QueryExecutionId']

while True:
    query_stats = client.get_query_execution(
        QueryExecutionId=query_execution_id
    )
    print query_stats
    if query_stats['QueryExecution']['Status']['State'] in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        break
    time.sleep(2)

print query_stats

results = client.get_query_results(
    QueryExecutionId=query_execution_id
)
print json.dumps(results)

for row in results['ResultSet']['Rows']:
    print ', '.join([d.get('VarCharValue', 'NULL') for d in row['Data']])



