class DoubleDict(dict):
    def __init__(self, double):
        super().__init__()
        for keys in double:
            assert type(keys) == tuple
            for key in keys:
                self[key] = double[keys]
