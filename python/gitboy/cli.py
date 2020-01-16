import requests
import argparse
import os

from .commands import issues, pull_requests

TOKEN = os.environ.get('GITHUB_TOKEN')

def get_args():
	parser = argparse.ArgumentParser(description="CLI tool to help manage Github stuff")
	subparsers = parser.add_subparsers(title="commands", dest="type")

	issues.add_command_parser(subparsers)
	pull_requests.add_command_parser(subparsers)

	return vars(parser.parse_args())

def get_issues():
	if TOKEN is None:
		raise ValueError("Token not found!")

	get_issues_req = requests.get("https://api.github.com/", headers={
		"Accept": "application/vnd.github.v3+json",
		"Authorization": f"token {TOKEN.strip()}"
	})

	return get_issues_req.json()

if __name__ == "__main__":
	args = get_args()
	# TODO: Add dispatch logic to send execution to correct handler
	if args['type'] == "issues":
		issues.IssueCommand(args).process()
		exit()


