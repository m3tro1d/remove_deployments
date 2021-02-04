# Script for removing deployments on GitHub
This is a fork of this gist https://gist.github.com/ewen-lbh/30f8237e218b14f0f40ca5ed13bf24d6 by [ewen-lbh](https://github.com/ewen-lbh). This handy script saved my day, so I decided to extend its capabilities.

This will delete deployments from the "Deployments" tab from github, using the endpoints documented at: https://developer.github.com/v3/repos/deployments/#delete-a-deployment

See https://stackoverflow.com/a/61272173/9943464 for more information.

## Requirements
- [Python 3](https://www.python.org/)
- [requests](https://pypi.org/project/requests/)

## Usage
**PLEASE MAKE SURE YOU DISCONNECTED YOUR SERVICES (GitHub, Heroku, etc.) BEFORE PROCEEDING.**

Make sure you use a personal access token that has 'repo_deployments' authorized.

```
Usage: remove_deployments.py [OPTIONS] URL TOKEN

URL:
  URL of a repository in the format of owner/repo

TOKEN
  Your GitHub personal access token.
  Make sure it has 'repo_deployments' authorized.

Options:
  -h,  --help   show help
  -a,  --all    delete ALL deployments, including the active ones (def: False)
```
