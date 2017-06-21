#!/usr/local/bin/python

import os
import sys
import argparse
import atexit
import readline
import uuid
import time
import json

import boto3
import cmd2 as cmd

from botocore.exceptions import ClientError, ParamValidationError
from tabulate import tabulate

AWS_REGION = 'eu-west-1'  # FIXME: use region in profile
S3_RESULTS_BUCKET = 's3://ophan-query-results'  # FIXME: use profile eg. s3://<profile>-query-results
HISTORY_FILE_SIZE = 500

__version__ = '0.0.2'

del cmd.Cmd.do_show


class AthenaShell(cmd.Cmd):

    multilineCommands = ['WITH', 'SELECT', 'ALTER', 'CREATE', 'DESCRIBE', 'DROP', 'MSCK', 'SHOW', 'USE', 'VALUES']
    allow_cli_args = False

    def __init__(self, region, bucket, db=None, debug=False):
        cmd.Cmd.__init__(self)

        self.region = region
        self.bucket = bucket
        self.dbname = db
        self.debug = debug

        self.execution_id = None
        self.row_count = 0

        self.athena = boto3.client('athena')
        self.set_prompt()

        self.hist_file = os.path.join(os.path.expanduser("~"), ".athena_history")
        self.init_history()

    def set_prompt(self):
        self.prompt = 'athena:%s> ' % self.dbname if self.dbname else 'athena> '

    def cmdloop_with_cancel(self, intro=None):
        try:
            self.cmdloop(intro)
        except KeyboardInterrupt:
            if self.execution_id:
                self._stop_query_execution()
                print('\n\n%s' % self._console_link())
                print('\nQuery aborted by user')
            else:
                print('\r')
            self.cmdloop_with_cancel(intro)

    def preloop(self):
        if os.path.exists(self.hist_file):
            readline.read_history_file(self.hist_file)

    def postloop(self):
        self.save_history()

    def init_history(self):
        try:
            readline.read_history_file(self.hist_file)
            readline.set_history_length(HISTORY_FILE_SIZE)
            readline.write_history_file(self.hist_file)
        except IOError:
            readline.write_history_file(self.hist_file)

        atexit.register(self.save_history)

    def save_history(self):
        try:
            readline.write_history_file(self.hist_file)
        except IOError:
            pass

    def do_help(self, args):
        help = """
Supported commands:
QUIT
SELECT
ALTER DATABASE <schema>
ALTER TABLE <table>
CREATE DATABASE <schema>
CREATE TABLE <table>
DESCRIBE <table>
DROP DATABASE <schema>
DROP TABLE <table>
MSCK REPAIR TABLE <table>
SHOW COLUMNS FROM <table>
SHOW CREATE TABLE <table>
SHOW DATABASES [LIKE <pattern>]
SHOW PARTITIONS <table>
SHOW TABLES [IN <schema>] [<pattern>]
SHOW TBLPROPERTIES <table>
USE [<catalog>.]<schema>
VALUES row [, ...]

See http://docs.aws.amazon.com/athena/latest/ug/language-reference.html
"""
        print(help)

    def do_quit(self, args):
        print
        return -1

    def do_EOF(self, args):
        return self.do_quit(args)

    def do_use(self, schema):
        self.dbname = schema.rstrip(';')
        self.set_prompt()

    def default(self, query):
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

        sys.stdout.write('\r')  # delete query status line
        sys.stdout.flush()

        if status == 'SUCCEEDED':
            print(tabulate([x for x in self._get_query_results()], headers=self.headers, tablefmt="orgtbl"))
            print('(%s rows)' % self.row_count)

        print('\nQuery {0}, {1}'.format(self.execution_id, status))
        if status == 'FAILED':
            print(stats['QueryExecution']['Status']['StateChangeReason'])
        print(self._console_link())

        submission_date = stats['QueryExecution']['Status']['SubmissionDateTime']
        completion_date = stats['QueryExecution']['Status']['CompletionDateTime']
        execution_time = stats['QueryExecution']['Statistics']['EngineExecutionTimeInMillis']
        data_scanned = stats['QueryExecution']['Statistics']['DataScannedInBytes']
        query_cost = data_scanned / 1000000000000.0 * 5.0

        print('Time: {}, CPU Time: {}ms total, Data Scanned: {}, Cost: ${:,.2f}\n'.format(
            str(completion_date - submission_date).split('.')[0],
            execution_time,
            human_readable(data_scanned),
            query_cost)
        )

    def _start_query_execution(self, query):
        try:
            return self.athena.start_query_execution(
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
            return self.athena.get_query_execution(
                QueryExecutionId=self.execution_id
            )
        except ClientError as e:
            print(e)

    def _get_query_results(self):
        try:
            results = self.athena.get_query_results(
                QueryExecutionId=self.execution_id
            )
        except ClientError as e:
            sys.exit(e)

        if self.debug:
            print(json.dumps(results, indent=2))

        self.headers = [h['Name'] for h in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        self.row_count = len(results['ResultSet']['Rows'])

        for row in results['ResultSet']['Rows']:
            if row['Data'][0]['VarCharValue'] == self.headers[0]:  # https://forums.aws.amazon.com/thread.jspa?threadID=256505
                self.row_count -= 1
                continue
            yield [d.get('VarCharValue', 'NULL') for d in row['Data']]

    def _stop_query_execution(self):
        try:
            return self.athena.stop_query_execution(
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


def main():

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

    if args.debug:
        boto3.set_stream_logger(name='botocore')

    if args.version:
        print('Athena CLI %s' % __version__)
        sys.exit()

    shell = AthenaShell(args.region, args.bucket, args.schema, args.debug)
    shell.cmdloop_with_cancel()

if __name__ == '__main__':
    main()
