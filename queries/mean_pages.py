# An example analysis, for determining average pages per book

def mapper(book):
    return [1, book.pages]

reducer=double_sum
