#!/usr/bin/env python

import os
import sys
import json
import socket

from datetime import datetime
from prettytable import PrettyTable

AWS_ACCOUNT_ID = 'YOUR_ACCOUNT_ID'

instances = json.loads(os.popen('aws rds describe-db-instances').read())

args = sys.argv
args.pop(0)

if len(args) and args[0] == '--tags':
    show_tags = True
    args.pop(0)
else:
    show_tags = False

if show_tags:
    t = PrettyTable(["Stage", "Stack", "App", "Instance", "IP Addr (Pub)", "IP Addr (Priv)", "Tags"])
    t.align["Stage"] = "l"
    t.align["Stack"] = "l"
    t.align["App"] = "l"
    t.align["Tags"] = "l"
else:
    t = PrettyTable(["Stage", "Stack", "App", "Instance", "Hostname", "IP Address", "Port", "AZ", "Instance Class", "Engine", "Ver.", "Username", "Launched", "Status", "Role"])
    t.align["Stage"] = "l"
    t.align["Stack"] = "l"
    t.align["App"] = "l"
    t.align["IP Address"] = "l"

match = args

sorted_instances = sorted(instances['DBInstances'], key=lambda i: i.get('InstanceCreateTime', '-'))

for i in sorted_instances:

    arn = 'arn:aws:rds:%s:%s:db:%s' % ('eu-west-1', AWS_ACCOUNT_ID, i['DBInstanceIdentifier'])
    tags = json.loads(os.popen('aws rds list-tags-for-resource --resource-name %s' % arn).read())
    for tag in tags['TagList']:
        if tag['Key'] == 'Stage':
            stage = tag['Value']
        if tag['Key'] == 'Stack':
            stack = tag['Value']
        if tag['Key'] == 'App':
            app = tag['Value']
        if tag['Key'] == 'aws:cloudformation:logical-id':
            role = tag['Value']

    # if 'StatusInfos' in i:
    #     role = i['StatusInfos'][0]['Status']
    # else:
    #     role = '-'

    t.add_row([
        stage,
        stack,
        app,

        i['DBInstanceIdentifier'],
        i['Endpoint']['Address'].replace('eu-west-1.rds.amazonaws.com','') if 'Endpoint' in i else '-',
        socket.gethostbyname(i['Endpoint']['Address']) if 'Endpoint' in i else '-',
        i['Endpoint']['Port'] if 'Endpiont' in i else '-',

        i['AvailabilityZone'],
        i['DBInstanceClass'],
        i['Engine'],
        i['EngineVersion'],

        i['MasterUsername'],
        i.get('InstanceCreateTime', '-'),
        i['DBInstanceStatus'],
        'none' #role or 'None'
    ])

print t


