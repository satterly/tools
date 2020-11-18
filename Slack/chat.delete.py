#!python
import json

import sys
import time
import requests

from datetime import datetime, timedelta

token = 'xoxp-3236328412-3236328416-1502621830757-f3fea9164b98b69340e837e6e3a5717f'  # oauth
# token = 'xoxb-3236328412-1490969405799-YAdnzkGQGi7oEZW2FedCLvMD'  # bot
# channel = 'C036X0JM7' # alerts
channel = 'G01FC03TKFA' #actions
# channel = 'C012X825E72' #deploys
# channel = 'C011KF5AJQN' #issues

r = requests.get(
    url='https://slack.com/api/conversations.info?channel={}'.format(channel),
    headers={'Authorization': 'Bearer {}'.format(token)}
)

if r.json()['ok']:
    print('Found {}'.format(r.json()['channel']['name']))
else:
    sys.exit(r.json()['error'])

ago = int((datetime.now() - timedelta(hours=2)).timestamp())

# use "latest" to delete old messages, ie. messages older than the give epoch seconds

r = requests.get(
    url='https://slack.com/api/conversations.history?channel={}&latest={}'.format(channel, ago),
    headers={'Authorization': 'Bearer {}'.format(token)}
)
print()
if r.json()['ok']:
    conversation = r.json()
    print('{} messages'.format(len(conversation)))
    print(json.dumps(conversation, indent=2))
else:
    sys.exit(r.json()['error'])

for message in [c for c in conversation['messages'] if c.get('subtype', 'none') == 'bot_message']:
# for message in [c for c in conversation['messages'] if True]:
    print(json.dumps(message, indent=2))
    print('Deleting {} - {}'.format(message['ts'], message['text']))
    r = requests.post(
        url='https://slack.com/api/chat.delete',
        json={'channel': channel, 'ts': message['ts']},
        headers={
            'Content-type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    print(r.json())
    time.sleep(1)