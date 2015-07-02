import yaml

class parser():
    def __init__(self, path):
        content=yaml.load(open(path))
        self.data=[[year, book] for year, books in content.iteritems() for book in books]
    def __len__(self):
        return len(self.data)
    def __getitem__(self,index):
        return self.data[index] 

def mapper(data):
    year, book=data
    return {year: len(book[4])}

reducer=merge_under(add)

