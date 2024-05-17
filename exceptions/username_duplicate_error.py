class UsernameDuplicateError(Exception):
    def __init__(self, msg):
        self.msg = msg