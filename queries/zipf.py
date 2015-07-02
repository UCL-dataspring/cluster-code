def mapper(book):
    finds=defaultdict(int)
    for word in book.words():
        finds[normalize(word)]+=1
    return finds

reducer=merge_under(add)

def shuffler(word, count):
    return hash(word)%count
