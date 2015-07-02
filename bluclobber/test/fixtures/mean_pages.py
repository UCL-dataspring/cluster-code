# An example analysis, for determining average pages per book

def mapper(book):
    return [1, book.pages]

def reducer(x, y):
    return [x[0]+y[0],x[1]+y[1]]
