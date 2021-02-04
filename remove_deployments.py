"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

from sys import exit
import requests

print("""
                                     _ _     _
        _____      _____ _ __       | | |__ | |__
       / _ \ \ /\ / / _ \ '_ \ _____| | '_ \| '_ \
      |  __/\ V  V /  __/ | | |_____| | |_) | | | |
       \___| \_/\_/ \___|_| |_|     |_|_.__/|_| |_|
                              QUICK & DIRTY SCRIPTS


                       ⚠ WARNING ⚠
              PLEASE MAKE SURE YOU DISCONNECTED
             YOUR SERVICES (GitHub, Heroku, etc.)
                   BEFORE PROCEEDING.

This will _delete_ deployments from the "Deployments" tab from github,
using the endpoints documented at:
https://developer.github.com/v3/repos/deployments/#delete-a-deployment

Make sure you use a personal access token that has
`repo_deployments` authorized.

See https://stackoverflow.com/a/61272173/9943464 for more information.


Licensed under the Unlicensed license (see the beginning of the file)
""")

OWNER = input('OWNER/repo => ')
if '/' in OWNER:
  OWNER, REPO = OWNER.split('/')
else:
  REPO = input('owner/REPO => ')
TOK = input('Personal access token => ')

url = lambda end: f'https://api.github.com/repos/{OWNER}/{REPO}/deployments{end}'

print(f'Running with base url: {url("")}')

# The token needs to be sent in this request too for private repos (thanks mxcl@so)
all_ids = [ deploy['id'] for deploy in requests.get(url(''), headers={'Authorization': f'token {TOK}'}).json() ]
if not all_ids:
  print('No deployments found.')
  exit(0)
print(f'Got deployments with IDs: {all_ids}')

for deploy_id in all_ids:
  # Set to inactive
  print(f'POST {url("")}{deploy_id}/statuses state=inactive')
  requests.post(
    url(f'/{deploy_id}/statuses'),
    {'state': 'inactive'},
    headers={
      'Authorization': f'token {TOK}',
      'Accept': 'application/vnd.github.ant-man-preview+json'
    }
  )
  # Delete
  print(f'DELETE {url("")}/{deploy_id}')
  requests.delete(url('/'+str(deploy_id)), headers={'Authorization': f'token {TOK}'})
