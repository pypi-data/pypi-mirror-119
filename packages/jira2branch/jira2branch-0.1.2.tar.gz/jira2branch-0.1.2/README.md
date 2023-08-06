# JIRA 2 Branch

Takes a JIRA issue and creates a git branch

- Branch naming format is as follows:
  - {CONVENTIONAL_COMMIT_PREFIX}/{ISSUE_ID}_{ISSUE_TITLE}

## Requirements

Requires Python 3.8

### Dev env

```
pip install pipenv
pipenv install
virtualenv venv
. venv/bin/activate
pip install --editable .
```

Afterwards, your command should be available:

```
$ jira2branch WT3-227
fix/WT3-227_some-jira-issue
```

### Credentials

JIRA credentials will be fetched from `[USER HOME]/.j2b/secrets.ini` with the following format:

```ini
[JIRA CREDENTIALS]

# url = 
# email = 
# username = 
# password = 
# token = 
```

## Usage

`python main.py [JIRA_ISSUE_ID|JIRA_ISSUE_URL]`

### Examples

`python main.py WT3-227`

`python main.py https://company.atlassian.net/browse/WT3-227`
