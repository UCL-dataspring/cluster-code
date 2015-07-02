import yaml

class parser():
    def __init__(self, path):
        content=yaml.load(open(path))
        self.data=[book.append(year) for year, books in content.iteritems() for book in books]
    def __len__(self):
        return len(self.data)
    def __getitem__(self,index):
        return self.data[index] 

def mapper(book):
    print "Book: " , book
    return (book[5],len(book[4]))

reducer=add
