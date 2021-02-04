# from sys import exit
# import requests

# print("""
#                                      _ _     _
#         _____      _____ _ __       | | |__ | |__
#        / _ \ \ /\ / / _ \ '_ \ _____| | '_ \| '_ \
#       |  __/\ V  V /  __/ | | |_____| | |_) | | | |
#        \___| \_/\_/ \___|_| |_|     |_|_.__/|_| |_|
#                               QUICK & DIRTY SCRIPTS


#                        ⚠ WARNING ⚠
#               PLEASE MAKE SURE YOU DISCONNECTED
#              YOUR SERVICES (GitHub, Heroku, etc.)
#                    BEFORE PROCEEDING.

# This will _delete_ deployments from the "Deployments" tab from github,
# using the endpoints documented at:
# https://developer.github.com/v3/repos/deployments/#delete-a-deployment

# Make sure you use a personal access token that has
# `repo_deployments` authorized.

# See https://stackoverflow.com/a/61272173/9943464 for more information.


# Licensed under the Unlicensed license (see the beginning of the file)
# """)

# OWNER = input('OWNER/repo => ')
# if '/' in OWNER:
#   OWNER, REPO = OWNER.split('/')
# else:
#   REPO = input('owner/REPO => ')
# TOK = input('Personal access token => ')

# url = lambda end: f'https://api.github.com/repos/{OWNER}/{REPO}/deployments{end}'

# print(f'Running with base url: {url("")}')

# # The token needs to be sent in this request too for private repos (thanks mxcl@so)
# all_ids = [ deploy['id'] for deploy in requests.get(url(''), headers={'Authorization': f'token {TOK}'}).json() ]
# if not all_ids:
#   print('No deployments found.')
#   exit(0)
# print(f'Got deployments with IDs: {all_ids}')

# for deploy_id in all_ids:
#   # Set to inactive
#   print(f'POST {url("")}{deploy_id}/statuses state=inactive')
#   requests.post(
#     url(f'/{deploy_id}/statuses'),
#     {'state': 'inactive'},
#     headers={
#       'Authorization': f'token {TOK}',
#       'Accept': 'application/vnd.github.ant-man-preview+json'
#     }
#   )
#   # Delete
#   print(f'DELETE {url("")}/{deploy_id}')
#   requests.delete(url('/'+str(deploy_id)), headers={'Authorization': f'token {TOK}'})
from textwrap import dedent
import argparse
import sys

import requests


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CustomArgumentParser(argparse.ArgumentParser):
    """Override ArgumentParser's help message"""
    def format_help(self):
        help_text = dedent(f"""\
        A handy script for removing the deployments from GitHub repositories.

        Usage: {self.prog} [OPTIONS] URL TOKEN

        URL:
          URL of a repository in the format of owner/repo

        TOKEN
            Your GitHub personal access token.
            Make sure it has 'repo_deployments' authorized.

        Options:
          -h,  --help   show help
          -a,  --all    delete ALL deployments, including the active ones (def: {self.get_default("all")})

        For more information visit:
        https://github.com/m3tro1d/remove_deployments
        """)
        return help_text

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def url_formatter(owner, repo):
    """Generates a URL pattern function"""
    return (lambda end="": f'https://api.github.com/repos/{owner}/{repo}/deployments{end}')


def valid_url(string):
    """Returns a tuple of (owner, repo) from the URL string"""
    if "/" in string:
        owner, repo = string.split("/")
    else:
        error = f"Invalid URL: {string}"
        raise argparse.ArgumentTypeError(error)
    return (owner, repo)


def parse_args():
    """Process input arguments"""
    parser = CustomArgumentParser(usage="%(prog)s [OPTIONS] URL TOKEN")

    parser.add_argument("-a", "--all", action="store_true")

    parser.add_argument("url", type=valid_url)

    parser.add_argument("token")

    return parser.parse_args()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    """Main function"""
    # Requests headers
    headers={
      "Authorization": f"token {args.token}",
      "Accept": "application/vnd.github.ant-man-preview+json"
    }
    # Get the URL formatting function
    url = url_formatter(*args.url)

    # Get all deployments
    response = requests.get(url(), headers=headers)
    response.raise_for_status()
    all_ids = [ deploy["id"] for deploy in response.json() ]
    if not all_ids:
        print("No deployments found.")
        sys.exit(0)
    print(f"Got deployments with IDs: {all_ids}")

    # Delete the deplyoments
    for deploy_id in all_ids:
        # Set the status to 'inactive', if we want to delete everything
        if args.all:
            print(f"POST {url()}/{deploy_id}/statuses state=inactive")
            requests.post(
                url(f"/{deploy_id}/statuses"),
                {"state": "inactive"},
                headers=headers
            )
        # Delete
        print(f"DELETE {url()}/{deploy_id}")
        requests.delete(
            url(f"/{deploy_id}"),
            headers=headers
        )


# Entry point
if __name__ == "__main__":
    args = parse_args()

    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupt", file=sys.stderr)
        sys.exit(1)
