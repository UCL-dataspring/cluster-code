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
    
    def checker(page, word):
        normalised=normalize(word)
        if normalised in diseases:
            return page, word
    return book.describe_relevant(book.scan_words(), checker)

reducer=merge_under(add)

def shuffler(word, count):
    return hash(word)%count


