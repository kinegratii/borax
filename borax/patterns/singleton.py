class MetaSingleton(type):
    def __init__(cls, *args):
        type.__init__(cls, *args)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = type.__call__(cls, *args, **kwargs)
        return cls.instance
