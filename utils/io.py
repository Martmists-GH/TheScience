import ujson as json


class JSONFile:
    def __init__(self, path):
        self.path = path
        with open(path) as f:
            self.data = json.load(f)

    def __setitem__(self, key, value):
        self.data[key] = value
        with open(self.path, "w") as f:
            json.dump(self.data, f)

    def __getattr__(self, item):
        return getattr(self.data, item)

    def __getitem__(self, item):
        return self.data[item]

    def __contains__(self, item):
        return self.data.__contains__(item)


class AttrDict:
    def __init__(self, dict_):
        for k, v in dict_.items():
            if isinstance(v, dict):
                dict_[k] = AttrDict(v)

        self.dict_ = dict_

    def __getattr__(self, item):
        try:
            return getattr(self.dict_, item)
        except AttributeError:
            return self.dict[item]
