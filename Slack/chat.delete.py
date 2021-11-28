#!python
import json
import os
from datetime import datetime

import sys
import time
import requests

from datetime import datetime, timedelta

deleted = 0

token = os.environ['SLACK_TOKEN']

C_ALERTS  = 'C036X0JM7' # alerts
C_ACTIONS = 'G01FC03TKFA' #actions
C_DEPLOYS = 'C012X825E72' #deploys
C_ISSUES  = 'C011KF5AJQN' #issues
C_PULLS   = 'C01EV76L1D3' #pull-requests

CHANNELS = [
    (C_ALERTS, 2),   # channel and keep days
    (C_ACTIONS, 1),
    (C_DEPLOYS, 3),
    (C_ISSUES, 7),
    (C_PULLS, 1),
]


def delete_message(channel, message):
    ts = datetime.fromtimestamp(float(message['ts']))
    print(f"{channel} Deleting {ts} - {message['text'] or message['attachments'][0]['fallback']}")
    r = requests.post(
        url='https://slack.com/api/chat.delete',
        json={'channel': channel, 'ts': message['ts']},
        headers={
            'Content-type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    return r.json()

for channel, keep_days in CHANNELS:

    r = requests.get(
        url='https://slack.com/api/conversations.info?channel={}'.format(channel),
        headers={'Authorization': 'Bearer {}'.format(token)}
    )

    if r.json()['ok']:
        name = r.json()['channel']['name']
        print('Found #{} ({}), delete after {} days'.format(name, channel, keep_days))
    else:
        sys.exit(r.json()['error'])

    ago = int((datetime.now() - timedelta(days=keep_days)).timestamp())

    # use "latest" to delete old messages, ie. messages older than the give epoch seconds

    r = requests.get(
        url='https://slack.com/api/conversations.history?channel={}&latest={}'.format(channel, ago),
        headers={'Authorization': 'Bearer {}'.format(token)}
    )
    if r.json()['ok']:
        conversation = r.json()
        print('{} conversations'.format(len(conversation)))
        # print(json.dumps(conversation, indent=2))
    else:
        sys.exit(r.json()['error'])

    #for message in [c for c in conversation['messages'] if c.get('subtype', 'none') == 'bot_message']:
    for message in conversation['messages']:
        # for message in [c for c in conversation['messages'] if True]:
        #print(json.dumps(message, indent=2))
        r = delete_message(channel, message)
        if r['ok']:
            deleted += 1
        # time.sleep(1)

print('Deleted {} messages'.format(deleted))
