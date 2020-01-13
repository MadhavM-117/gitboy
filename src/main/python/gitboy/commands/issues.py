import argparse

def add_command_parser(subparsers: argparse._SubParsersAction):
	"""
	Function to add the relevant parser for the command
	Args:
		subparsers: subparser to add arguments to
	"""
	issue_parser = subparsers.add_parser("issues")
	issue_sub_parser = issue_parser.add_subparsers(title="sub-commands", dest="sub_type")

	all_parser = issue_sub_parser.add_parser("all")
	assigned_parser = issue_sub_parser.add_parser("assigned")

	mentioned_parser:argparse.ArgumentParser = issue_sub_parser.add_parser("mentioned")
	mentioned_parser.add_argument(
		"--no_reply", "-n", default=False, action="store_true", 
		help="View issues where you have been mentioned, but that you haven't replied to"
	)
	
	stale_parser: argparse.ArgumentParser = issue_sub_parser.add_parser("stale")
	stale_parser.add_argument(
		"-u", "--update_label", default=False, action="store_true", 
		help="Update stale issues with the stale label"
	)
	
	label_parser: argparse.ArgumentParser = issue_sub_parser.add_parser("label")
	label_parser.add_argument("label", type=str, help="Filter issues that have this label")

