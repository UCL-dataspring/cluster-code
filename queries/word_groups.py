groups=[('henry','james','roosevelt')]
chunk_length=12

def mapper(book):
    finds=defaultdict(list)
    for finding in groups_of(chunk_length,book.scan_words()):
        for group in groups:
            words=[normalize(word) for page, word in finding]
            contained=[target in words for target in group]
        if all(contained):
            finds[group].append([words, finding[0][0].code])
    result = {group: [[book.title, book.publisher, book.year, book.code, content]] 
            for group, content in finds.iteritems()}
    return result

reducer=merge_under(add)

