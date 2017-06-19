#!/usr/bin/env python

import os
import argparse
import requests


GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY', '')

GITHUB_ORG = 'guardian'

# Example
#
# $ GITHUB_API_KEY=04e0c66cffff949efc22f8b8efae0c6a2ebf33ec  ./team_keys.py --team Discussion


class ApiAuth(object):

    def __init__(self, token):

        self.token = token

    def __call__(self, r):

        r.headers['Authorization'] = 'token %s' % self.token
        return r


class GitHub(object):

    def __init__(self, token):

        self.token = token
        self.headers = {
            "Content-type": "application/json"
        }

    def list_team(self, team):

        team_id = [t['id'] for t in self._get('/orgs/%s/teams' % GITHUB_ORG) if t['name'] == team]
        return self._get('/teams/%s/members' % team_id[0])

    def get_user_key(self, user):

        return self._get('/users/%s/keys' % user)

    def _get(self, path):

        url = GITHUB_API_URL + path
        r = requests.get(url, headers=self.headers, auth=ApiAuth(self.token))
        return r.json()


def main(args):

    gh = GitHub(token=GITHUB_API_KEY)

    for member in gh.list_team(args.team):
        keys = gh.get_user_key(member['login'])
        print "### %s" % member['login']
        for k in keys:
            print k['key']

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--team')
    args = parser.parse_args()

    main(args)
