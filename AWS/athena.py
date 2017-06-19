#!/usr/local/bin/python

import os
import sys
import argparse
import atexit

import cmd
import readline
import uuid
import time
import json

import boto3
from botocore.exceptions import ClientError, ParamValidationError

from tabulate import tabulate


AWS_REGION = 'eu-west-1'
S3_RESULTS_BUCKET = 's3://ophan-query-results'

athena_client = boto3.client('athena')

HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".athena_history")
HISTORY_FILE_SIZE = 500

__version__ = '0.1'


class AthenaShell(cmd.Cmd):

    def __init__(self, region, bucket, db=None, debug=False):
        cmd.Cmd.__init__(self)

        self.region = region
        self.bucket = bucket
        self.dbname = db
        self.debug = debug
        self.execution_id = None

        self.set_prompt()
        atexit.register(self.save_history)

    def set_prompt(self):
        self.prompt = 'athena:%s> ' % self.dbname if self.dbname else 'athena> '

    def cmdloop_with_cancel(self, intro=None):
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            self._stop_query_execution()
            print('\n\n%s' % self._console_link())
            print('\nQuery aborted by user')
            self.cmdloop()

    def precmd(self, line):
        return line.lower()

    def preloop(self):
        if os.path.exists(HISTORY_FILE):
            readline.read_history_file(HISTORY_FILE)

    def postloop(self):
        self.save_history()

    def save_history(self):
        readline.set_history_length(HISTORY_FILE_SIZE)
        readline.write_history_file(HISTORY_FILE)

    def do_help(self, args):
        help = """
Supported commands:
QUIT
EXPLAIN [ ( option [, ...] ) ] <query>
    options: FORMAT { TEXT | GRAPHVIZ }
             TYPE { LOGICAL | DISTRIBUTED }
DESCRIBE <table>
SHOW COLUMNS FROM <table>
SHOW FUNCTIONS
SHOW CATALOGS [LIKE <pattern>]
SHOW SCHEMAS [FROM <catalog>] [LIKE <pattern>]
SHOW TABLES [FROM <schema>] [LIKE <pattern>]
SHOW PARTITIONS FROM <table> [WHERE ...] [ORDER BY ...] [LIMIT n]
USE [<catalog>.]<schema>

See http://docs.aws.amazon.com/athena/latest/ug/language-reference.html
"""
        print(help)

    def do_quit(self, args):
        print
        sys.exit()

    def do_EOF(self, args):
        return self.do_quit(args)

    def do_use(self, schema):
        self.dbname = schema.rstrip(';')
        self.set_prompt()

    def default(self, query):
        start_time = time.time()
        self.execution_id = self._start_query_execution(query)
        if not self.execution_id:
            return

        while True:
            stats = self._get_query_execution()
            status = stats['QueryExecution']['Status']['State']
            sys.stdout.write('\rQuery {0}, {1}'.format(self.execution_id, status))
            sys.stdout.flush()
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(0.2)  # 200ms

        sys.stdout.write('\rQuery {0}, {1}\n'.format(self.execution_id, status))
        sys.stdout.flush()

        if status == 'FAILED':
            print(stats['QueryExecution']['Status']['StateChangeReason'])

        execution_time = stats['QueryExecution']['Statistics']['EngineExecutionTimeInMillis']
        data_scanned = stats['QueryExecution']['Statistics']['DataScannedInBytes']
        query_cost = data_scanned / 1000000000000.0 * 5.0

        print(self._console_link())
        print('Execution Time: {}ms, Data Scanned: {}, Cost: ${:,.2f}'.format(execution_time, human_readable(data_scanned), query_cost))
        print(time.time() - start_time)

        submission_date = stats['QueryExecution']['Status']['SubmissionDateTime']
        completion_date = stats['QueryExecution']['Status']['CompletionDateTime']
        print(submission_date)
        print(completion_date)
        print(completion_date - submission_date)

        if status == 'SUCCEEDED':
            print tabulate([x for x in self._get_query_results()], headers=self.headers, tablefmt="orgtbl")

    def _start_query_execution(self, query):
        try:
            return athena_client.start_query_execution(
                QueryString=query,
                ClientRequestToken=str(uuid.uuid4()),
                QueryExecutionContext={
                    'Database': self.dbname
                },
                ResultConfiguration={
                    'OutputLocation': self.bucket
                }
            )['QueryExecutionId']
        except (ClientError, ParamValidationError) as e:
            print(e)
            return

    def _get_query_execution(self):
        try:
            return athena_client.get_query_execution(
                QueryExecutionId=self.execution_id
            )
        except ClientError as e:
            print(e)

    def _get_query_results(self):
        try:
            results = athena_client.get_query_results(
                QueryExecutionId=self.execution_id
            )
        except ClientError as e:
            sys.exit(e)

        if self.debug:
            print(json.dumps(results, indent=2))

        self.headers = [h['VarCharValue'] for h in results['ResultSet']['Rows'][0]['Data']]
        for row in results['ResultSet']['Rows'][1:]:
            yield [d.get('VarCharValue', 'NULL') for d in row['Data']]

    def _stop_query_execution(self):
        try:
            return athena_client.stop_query_execution(
                QueryExecutionId=self.execution_id
            )
        except ClientError as e:
            sys.exit(e)

    def _console_link(self):
        return 'https://{0}.console.aws.amazon.com/athena/home?force&region={0}#query/history/{1}'.format(self.region, self.execution_id)


def human_readable(size, precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='athena',
        usage='athena [--debug] [--execute <execute>] [--output-format <output-format>] [--schema <schema>] [--version]'
              ' [--region <region>] [--s3-bucket <bucket>]',
        description='Athena interactive console'
    )
    parser.add_argument(
        '--debug',
        action='store_true'
    )
    parser.add_argument(
        '--execute'
    )
    parser.add_argument(
        '--output-format'
    )
    parser.add_argument(
        '--schema',
        '--database',
        '--db'
    )
    parser.add_argument(
        '--version',
        action='store_true'
    )
    parser.add_argument(
        '--region',
        default=AWS_REGION
    )
    parser.add_argument(
        '--s3-bucket',
        '--bucket',
        dest='bucket',
        default=S3_RESULTS_BUCKET
    )
    args = parser.parse_args()

    if args.version:
        print('Athena CLI %s' % __version__)
        sys.exit()

    shell = AthenaShell(args.region, args.bucket, args.schema, args.debug)
    shell.cmdloop_with_cancel()
