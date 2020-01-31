import argparse

from gitboy.commands import issues


class ProcessDispatcher:
    def __init__(self, parser: argparse.ArgumentParser, parser_dict: dict):
        self.parser = parser
        self.parser_dict = parser_dict

    def dispatch(self):
        args = vars(self.parser.parse_args())
        if args.get("type") not in self.parser_dict.keys():
            self.parser.print_help()
            return 1

        if args.get("sub_type") is None:
            sub_parser = self.parser_dict[args["type"]]
            sub_parser.print_help()

        if args["type"] == "issues":
            issues.IssueCommand(args).process()
            return 0

        return 1
