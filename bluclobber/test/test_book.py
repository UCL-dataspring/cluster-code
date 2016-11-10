from unittest import TestCase
from lxml import etree

from ..archive import Archive
from ..book import Book
from .fixtures import path

class test_book(TestCase):
    def setUp(self):
        source=path('zips','book37m.zip')
        self.arc=Archive(source)
        self.book=self.arc[0]
        self.book.load()
    def test_title(self):
        assert "Love the Avenger" in self.book.title
    def test_place(self):
        assert "London" in self.book.place
    def test_code(self):
        assert self.book.code == '000000218'
        assert self.book.code in self.arc.book_codes
        assert '03_000002' in self.arc.book_codes[self.book.code]
    def test_page_codes(self):
        assert '03_000002' in self.book.page_codes
    def test_pages(self):
        assert self.book.pages==306
    def test_content(self):
        assert ("the great Avorld of Paris" in self.book[25].content)
    def test_year(self):
        assert self.book.years==[1823, 1869]
    def test_yearify(self):
        fixtures={
                "[1866]": [1866],
                "1885]":[1885],
                "1847 [1846, 47]":[1846, 1847],
                "1862, [1861]":[1861, 1862],
                "1873-80":[1873, 1880],
                "[ca. 1730]":[1730],
                "1725, 26":[1725, 1726],
        }
        for case, expected in fixtures.iteritems():
            assert Book.parse_year(case) == expected
