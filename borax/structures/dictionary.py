class AttributeDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            # to conform with __getattr__ spec
            raise AttributeError(key) from e

    def __setattr__(self, key, value):
        self[key] = value


AD = AttributeDict
