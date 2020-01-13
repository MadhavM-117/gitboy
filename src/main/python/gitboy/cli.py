import requests
import argparse
import os

TOKEN = os.environ.get('GITHUB_TOKEN')

def get_args():
	parser = argparse.ArgumentParser(description="CLI tool to help manage Github stuff")
	subparsers = parser.add_subparsers(title="commands")

	issue_parser = subparsers.add_parser("issue")
	
	issue_sub_parser = issue_parser.add_subparsers(title="sub-commands")
	list_parser = issue_sub_parser.add_parser("list")
	list_parser.add_argument("--all", "-a", default=False, action="store_true", help="List All Issues")

	return parser.parse_args()

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
	print(vars(args))
	print(TOKEN)
	print(get_issues())



