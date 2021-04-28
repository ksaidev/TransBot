class DoubleDict(dict):
    """
    A custom data structure for TransBot
    """
    def __init__(self, init):
        super().__init__()
        for keys in init:
            assert type(keys) == tuple
            for key in keys:
                self[key] = init[keys]
