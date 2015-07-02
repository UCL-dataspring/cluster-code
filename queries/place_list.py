def mapper(book):
    return {book.place: {book.year: 1}} 

reducer = merge_under(merge_under(add))

def shuffler(place, count):
    return hash(place)%count
