# "How does average word length change over time"

def mapper(book):
    count=len(list(book.words()))
    pages=book.pages
    return {book.year: [1, pages, count]}

reducer = merge_under(triple_sum)

def shuffler(year, count):
    return year%count
