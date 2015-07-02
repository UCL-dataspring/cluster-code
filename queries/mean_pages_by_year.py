# An example analysis, for determining average pages per book

def mapper(book):
    return {book.year: [1, book.pages]}

reducer=merge_under(double_sum)

def shuffler(year, count):
    return year%count
