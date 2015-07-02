from unittest import TestCase
from lxml import etree

from ...model.page import Page
from ..fixtures import path

class test_page(TestCase):
    def setUp(self):
        source=path('page.xml')
        self.page=Page(None, None, source)
    def test_content(self):
        assert("LOVE THE AVENGER" in self.page.content)
