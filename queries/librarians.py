interesting_words=map(lambda x: x.lower(),
    ['librarian',
    'librarians',
    ])


def mapper(book):
    def checker(page, word):
        word=normalize(word)
        if word in interesting_words:
            return page, word

    return book.describe_relevant(book.scan_words(), checker)

reducer=merge_under(add)

def shuffler(year, count):
    return year%count
