import os

def path(*name):
    return os.path.join(os.path.dirname(__file__),*name)

def file(*name):
    return open(path(*name))

def content(*name):
    with open(path(*name)) as ffile:
        result = file.read()
    return result
