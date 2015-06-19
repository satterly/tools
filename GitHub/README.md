
# Gissues

Use [Mac OSX User Notifications](https://support.apple.com/en-gb/HT204079) to display banners for GitHub issues. This was a feature of the [GitHub app](https://mac.github.com/) but it was removed due to it being "half-backed" [1].

![notification](/GitHub/docs/images/github-notification.png?raw=true)

Installation
------------

1. Copy script to ~/bin or /usr/local/bin
2. Install [terminal-notifier](https://github.com/alloy/terminal-notifier) using `brew install terminal-notifier`
3. Install the [GitHub app](https://mac.github.com/) to make issues appear in the GitHub app group
4. Create a [GitHub Personal access token](https://github.com/settings/tokens)
5. Add an entry to crontab to run the script on a schedule using `crontab -e`

```
0 10,11,12,14,15,16 * * 1-5 GITHUB_API_KEY=45bd2f509e7e25d806011a5b3503bafb7example /usr/local/bin/gissues.py

```

[1]: https://github.com/blog/1287-github-for-mac-notifications
