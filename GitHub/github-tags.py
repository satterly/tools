import os
import requests
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY', '')

owner = 'alerta'

labels = {
    'bug': 'd73a4a',
    'docs': '3b6eef',
    'duplicate': 'cccccc',
    'enhancement': '84b6eb',
    'good first issue': '7057ff',
    'help wanted': '159818',
    'invalid': 'e6e6e6',
    'question': 'cc317c',
    'wontfix': 'ffffff',
    'worksforme': 'fbca04'
}

headers = {
    'Authorization': 'token ' + GITHUB_API_KEY,
    'Content-Type': 'application/json'
}

r = requests.get(GITHUB_API_URL + '/orgs/{org}/repos'.format(org=owner), headers=headers)
repos = [r['name'] for r in r.json()]
print(repos)

for repo in repos:
    # for label in labels:
    #     payload = {
    #       "color": labels[label]
    #     }
    #     r = requests.patch(GITHUB_API_URL + '/repos/{owner}/{repo}/labels/{current_name}'.format(owner=owner, repo=repo, current_name=label), json=payload, headers=headers)
    #     print(r.json())
    #
    #     payload = {
    #         'name': 'docs',
    #         'color': labels['docs'],
    #         'description': 'This needs to be documented'
    #     }
    #     print(payload)
    #     r = requests.post(GITHUB_API_URL + '/repos/{owner}/{repo}/labels'.format(owner=owner, repo=repo), json=payload, headers=headers)
    #     print(r.json())

    payload = {
        'name': 'worksforme',
        'color': labels['worksforme'],
        'description': "This bug can't be reproduced"
    }
    print(payload)
    r = requests.post(GITHUB_API_URL + '/repos/{owner}/{repo}/labels'.format(owner=owner, repo=repo), json=payload, headers=headers)
    print(r.json())
