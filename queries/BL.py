phrase='British Library'

alpha=re.compile('[^a-zA-Z]')


def normalize_keep_case(word):
    return re.sub(alpha,'',word)

def mapper(book):
    
    def checker(first, second):
        first_word=normalize_keep_case(first[1])
        second_word=normalize_keep_case(second[1])
        page=first[0]
        if [first_word, second_word]==phrase_words:
            return page, [first[1], second[1]]
    
    return book.describe_relevant(groups_of(2, book.scan_words()), checker)

reducer=merge_under(add)

def shuffler(year, count):
    return year%count
