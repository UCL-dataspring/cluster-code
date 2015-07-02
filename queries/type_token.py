def mapper(book):
    words=list(book.words())
    token_count=len(words)
    types=set(words)
    year=book.year
    return {year: (token_count, types)}

def reduce_each_year(first, second):
    token_count=first[0]+second[0]
    types=first[1].union(second[1])
    return (token_count, types)

reducer = merge_under(reduce_each_year)

def reporter(result):
    # We don't actually want to record every unique word!
    return {year: [res[0],len(res[1])] for year, res in result.iteritems() }

def shuffler(year, count):
    # which years should be reduced on which process?
    # Must be stable on different numbers of years on different processes
    # so cannot just be a split by even chunks 
    return year%count
