#!/usr/local/bin/python

import os
import sys
import requests
import subprocess
import time

from requests.auth import AuthBase


GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY', '')

PAUSE_BETWEEN_NOTIFY = 5  # seconds


class ApiAuth(AuthBase):

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

    def repo_info(self, owner, repo):

        return self._get('/repos/%s/%s' % (owner, repo))

    def issues(self, filter='all'):

        return self._get('/issues?filter=%s' % filter)

    def issues_assigned(self):

        return self.issues('assigned')

    def issues_created(self):

        return self.issues('created')

    def issues_mentioned(self):

        return self.issues('mentioned')

    def issues_subscribed(self):

        return self.issues('subscribed')

    def user_issues(self, filter='all'):

        return self._get('/user/issues?filter=%s' % filter)

    def repo_issues(self, org, repo, filter='all'):

        return self._get('/repos/%s/%s/issues?filter=%s' % (org, repo, filter))

    def org_issues(self, org, filter='all'):

        return self._get('/orgs/%s/issues?filter=%s' % (org, filter))

    def repo_comments(self, org, repo, user, page=1):

        r = self._get('/repos/%s/%s/pulls/comments?page=%s' % (org, repo, page))

        comments = list()
        for c in r:
            if c['user']['login'] == user:
                comments.append(c)
        return comments

    def _get(self, path):

        url = GITHUB_API_URL + path

        r = requests.get(url, headers=self.headers, auth=ApiAuth(self.token))
        return r.json()




def notify(repo, number, title, updated, icon, url):

    cmd = [
        "/usr/local/bin/terminal-notifier",
        "-message", "\"%s\"" % title,
        "-title", "\"GitHub Issue\"",
        "-subtitle", "%s#%s" % (repo, number),
        "-group", repo,
        "-appIcon", icon,
        "-sender", "com.github.GitHub",
        "-open", url,
        "-sound", "Purr"
    ]
    #print (' ').join(cmd)
    try:
        retcode = subprocess.call(cmd, shell=False)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            #print >>sys.stderr, "Child returned", retcode
            pass
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e

    time.sleep(PAUSE_BETWEEN_NOTIFY)


def notify_issue(issue):

    print "%s %-34s %-50s" % (issue['updated_at'], issue['repository']['full_name'] + '#' + str(issue['number']), issue['title'])

    notify(repo=issue['repository']['full_name'],
           number=issue['number'],
           title=issue['title'].replace('"', '\\"'),
           updated=issue['updated_at'],
           icon=issue['repository']['owner']['avatar_url'],
           url=issue['html_url'])


def notify_repo_issue(issue, info):

    print "%s %-34s %-50s" % (issue['updated_at'], info['full_name'] + '#' + str(issue['number']), issue['title'])

    notify(repo=info['full_name'],
           number=issue['number'],
           title=issue['title'].replace('"', '\\"'),
           updated=issue['updated_at'],
           icon=info['owner']['avatar_url'],
           url=issue['html_url'])


def main():

    import sys
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    gh = GitHub(GITHUB_API_KEY)

    user = 'satterly'
    print "comments for guardian org for %s" % user
    for repo in ['discussion-api']:
        for page in range(1,100,1):
            print '<h2>Repo %s Page %s</h2>' % (repo, page)
            for comment in gh.repo_comments('guardian', repo, user, page):
                if comment['user']['login'] == user:
                    # print '%s %s %s %s' % (comment['user']['login'], comment['created_at'], comment['body'], comment['html_url'])
                    print '<div>'
                    print '%s %s <a href="%s">%s</a> %s'.encode('utf-8') % (comment['user']['login'], comment['created_at'], comment['html_url'], comment['id'], comment['body'])
                    print '</div>'
if __name__ == '__main__':
    main()
