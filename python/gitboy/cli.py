import requests
import argparse
import os

from .commands import issues, pull_requests

TOKEN = os.environ.get('GITHUB_TOKEN')

def get_parser():
	parser = argparse.ArgumentParser(description="CLI tool to help manage Github stuff")
	subparsers = parser.add_subparsers(title="commands", dest="type")

	issues.add_command_parser(subparsers)
	pull_requests.add_command_parser(subparsers)
	return parser


def get_args():
	parser = get_parser()

	return vars(parser.parse_args())


if __name__ == "__main__":
	parser = get_parser()
	args = vars(parser.parse_args())
	# @TODO: Add dispatch logic to send execution to correct handler
	if args['type'] == "issues":
		if not issues.IssueCommand(args).process():
			# @TODO: Add logic to display issue parser help
			pass
		exit()

	parser.print_help()
	