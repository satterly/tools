import os
import requests

GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY', '')

owner = 'alerta'
repo = 'alerta'

headers = {
    'Authorization': 'token ' + GITHUB_API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.github.v3.star+json'
}

pages = 50

for page in range(1, pages+1):
    r = requests.get(GITHUB_API_URL + '/repos/{org}/{repo}/stargazers?client_id=xxx&client_secret=yyy&page={page}'.format(org=owner, repo=repo, page=page), headers=headers)
    gazers = [(s['user']['login'], s['starred_at']) for s in r.json()]
    for g in gazers:
        r = requests.get(GITHUB_API_URL + '/users/{username}?client_id=xxx&client_secret=yyy'.format(username=g[0]))
        user = r.json()
        try:
            print('{starred_at} ; {login} ; {name} ; {company} ; {location} ; {email} ; {bio}'.format(starred_at=g[1], **user))
        except Exception:
            print(r.json()['message'])


