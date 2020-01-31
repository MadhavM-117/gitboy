import argparse
import os

from .commands import issues, pull_requests
from .utils.core import ProcessDispatcher

TOKEN = os.environ.get("GITHUB_TOKEN")
PARSERS = {}


def get_parser():
    parser = argparse.ArgumentParser(description="CLI tool to help manage Github stuff")
    subparsers = parser.add_subparsers(title="commands", dest="type")

    i_key, i_parser = issues.add_command_parser(subparsers)
    PARSERS[i_key] = i_parser

    pr_key, pr_parser = pull_requests.add_command_parser(subparsers)
    PARSERS[pr_key] = pr_parser

    return parser


def get_args():
    parser = get_parser()

    return vars(parser.parse_args())


if __name__ == "__main__":
    parser = get_parser()
    exit(ProcessDispatcher(parser, PARSERS).dispatch())
