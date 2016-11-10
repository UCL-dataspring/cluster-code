from unittest import TestCase
from lxml import etree

from .fixtures import path
from ..archive import Archive

class test_archive(TestCase):
    def setUp(self):
        source=open(path('zips','book37.zip'))
        self.arc=Archive(source)
    def test_books(self):
        assert(self.arc.book_codes.keys()==['000000218', '000000037'])
        assert('000001' in self.arc.book_codes['000000037'])
        assert('03_000002' in self.arc.book_codes['000000218'])
    def test_pages(self):
        assert(len(self.arc.book_codes['000000037'])==42)
