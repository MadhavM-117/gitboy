class BaseCommand:
    def __init__(self, args: dict):
        self.args = args
        self.type = args["type"]
        self.sub_type = args["sub_type"]

    def validate(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError
