class DoubleDict(dict):
    def __init__(self, init):
        super().__init__()
        for keys in init:
            assert type(keys) == tuple
            for key in keys:
                self[key] = init[keys]

    # def __setitem__(self, keys, value):
    #     assert type(keys) == tuple
    #     for key in keys:
    #         self[key] = value
