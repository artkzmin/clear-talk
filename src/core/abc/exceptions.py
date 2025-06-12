class BaseException(Exception):
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)
