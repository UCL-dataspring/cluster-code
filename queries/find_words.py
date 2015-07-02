interesting_words=map(lambda x: x.lower(),
    ['professor',
    'utilitarian',
    'americanism',
    'librarian',
    'cholera'])

def mapper(book):

    def checker(page, word):
        if normalize(word) in interesting_words:
            return page, word

    return book.describe_relevant(book.scan_words(), checker)

reducer=merge_under(add)

def shuffler(word, count):
    return hash(word)%count
