def mapper(book):
    return set(element.tag for element in book.scan_elements())

def reducer(a, b):
    return a.union(b)
