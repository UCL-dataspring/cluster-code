
def mapper(book):
    scanner=groups_of(2,book.scan_words())

    def checker(first, second):
        page, word1=first
        _, word2=second
        nword1=normalize(word1)
        nword2=normalize(word2)

        if (nword2 in ['manager','managers']
            and nword1 not in ['waste','quarry']):
            return [page, [word1, word2 ]]
    
    return book.describe_relevant(scanner, checker)

reducer=merge_under(add)

def shuffler(item, count):
    return hash(item)%count
