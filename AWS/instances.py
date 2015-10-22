#!/usr/bin/env python

import os
import sys
import json

from datetime import datetime
from prettytable import PrettyTable

# aws ec2 describe-instances | jq '.Reservations[].Instances[] | { Stage: .Tags[] | select(.Key == "Stage") | .Value, Stack: .Tags[] | select(.Key == "Stack") | .Value, App: .Tags[] | select(.Key == "App") | .Value, InstanceId: .InstanceId, IpAddress: .PrivateIpAddress, AZ: .Placement.AvailabilityZone, InstanceType: .InstanceType, Virtualisation: .VirtualizationType, Launch: .LaunchTime, Status: .State.Name } | join(" | ") ' | sort | cut -c2- | sed 's/"$//' | column -t -s "|"

instances = json.loads(os.popen('aws ec2 describe-instances').read())
checks = json.loads(os.popen('aws ec2 describe-instance-status').read())

status = dict()
for c in checks['InstanceStatuses']:
    status[c['InstanceId']] = "%s/%s" % (c['SystemStatus']['Status'].replace('initializing', 'init'), c['InstanceStatus']['Status'].replace('initializing', 'init'))

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
    t = PrettyTable(["Stage", "Stack", "App", "Instance", "IP Addr (Pub)", "IP Addr (Priv)", "AZ", "Instance Type", "AMI", "Virtualisation", "Root", "Launched", "Status", "Checks"])
    t.align["Stage"] = "l"
    t.align["Stack"] = "l"
    t.align["App"] = "l"
    t.align["IP Address"] = "l"

match = args

sorted_instances = list()
for r in instances['Reservations']:
    for i in r['Instances']:
        sorted_instances.append(i)
sorted_instances = sorted(sorted_instances, key=lambda i: i['LaunchTime'])

for i in sorted_instances:
    if match and not all(word in str(i) for word in match):
            continue
    tags = dict([(tag['Key'], tag['Value']) for tag in i.get('Tags',{})])
    if show_tags:
        t.add_row([
            tags.get('Stage', 'none'),
            tags.get('Stack','none'),
            tags.get('App', 'none'),
            i['InstanceId'],
            i.get('PublicIpAddress', 'none'),
            i.get('PrivateIpAddress', 'none'),
            ', '.join('%s=%s' % t for t in tags.items() if t[0] not in ['Stage', 'Stack', 'App'] and not t[0].startswith('aws:'))
        ])
    else:
        t.add_row([
            tags.get('Stage', 'none'),
            tags.get('Stack','none'),
            tags.get('App', 'none'),
            i['InstanceId'],
            i.get('PublicIpAddress', 'none'),
            i.get('PrivateIpAddress', 'none'),
            i['Placement']['AvailabilityZone'],
            i['InstanceType'],
            i['ImageId'],
            i['VirtualizationType'],
            i['RootDeviceType'],
            datetime.strptime(i['LaunchTime'],
            "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%a %d %b %H:%M:%S'),
            i['State']['Name'],
            status.get(i['InstanceId'], 'n/a')
        ])

print t
