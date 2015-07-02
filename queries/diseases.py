diseases=set([
        'cholera',
        'tuberculosis',
        'consumption',
        'phthisis',
        'typhoid',
        'whooping',
        'measles',
        'typhus',
        'smallpox',
        'diarrhoea',
        'dysentry',
        'diphtheria',
        'cancer'
        ])

def mapper(book):
    finds=defaultdict(list)
    for page, word in book.scan_words():
        normalised=normalize(word)
        if normalised in diseases:
            finds[normalised].append(page.code)
    result = {word: {book.year: len(pages)} for word, pages in finds.iteritems()}
    return result

reducer=merge_under(merge_under(add))

def shuffler(word, count):
    return hash(word)%count

