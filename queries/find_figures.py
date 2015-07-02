def mapper(book):
    def checker(page, element):
        width=int(element.get('WIDTH'))
        height=int(element.get('HEIGHT'))
        x=int(element.get('HPOS'))
        y=int(element.get('VPOS'))
        area=width*height
        fracarea=area/(page.width*page.height)
        return page, [width, height, x, y, fracarea]

reducer=merge_under(add)

def shuffler(year, count):
    return year%count

