def mapper(book):
    finds=defaultdict(list)
    for page,element in book.scan_images():
        width=int(element.get('WIDTH'))
        height=int(element.get('HEIGHT'))
        x=int(element.get('HPOS'))
        y=int(element.get('VPOS'))
        area=width*height
        fracarea=area/(page.width*page.height)
        finds[book.year].append([book.summary, page.code])
    return dict(finds)

reducer=merge_under(add)

def shuffler(year, count):
    return year%count
