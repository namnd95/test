
config = {}


def get(name):
    return config[name]


def update(module):
    name = module.__name__
    name = name[name.rfind('.') + 1:]
    config[name] = module
