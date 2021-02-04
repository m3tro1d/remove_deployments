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
        PLEASE MAKE SURE YOU DISCONNECTED
        YOUR SERVICES (GitHub, Heroku, etc.)
        BEFORE PROCEEDING.

        This will delete deployments from the "Deployments" tab from github,
        using the endpoints documented at:
        https://developer.github.com/v3/repos/deployments/#delete-a-deployment

        Make sure you use a personal access token that has
        'repo_deployments' authorized.

        See https://stackoverflow.com/a/61272173/9943464 for more information.


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
    return lambda end="": f'https://api.github.com/repos/{owner}/{repo}/deployments{end}'


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
