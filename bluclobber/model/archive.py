import zipfile
import re

from book import Book

from cStringIO import StringIO

import logging

class Archive(object):
    def __init__(self, path):
        self.path = path
        self.logger=logging.getLogger('performance')
        self.logger.info("Opening archive " + path)
        with open(path) as finfo:
            self.logger.debug("Opened archive")
            mmap=StringIO(finfo.read())
            self.logger.info("Slurped archive")
            self.zip = zipfile.ZipFile(mmap)
        self.logger.debug("Examining books in archive")
        self.filenames = [entry.filename for entry in self.zip.infolist()]
        book_pattern = re.compile('([0-9]*)_metadata\.xml')
        page_pattern = re.compile('ALTO\/([0-9]*?)_([0-9_]*)\.xml')
        self.logger.debug("Enumerating books")
        bookmatches=filter(None, [ book_pattern.match(name) for name in self.filenames ])
        pagematches=filter(None, [ page_pattern.match(name) for name in self.filenames ])
        self.book_codes={ match.group(1) : [] for match in bookmatches }
        for match in pagematches:
            self.book_codes[ match.group(1) ].append(match.group(2))
        self.logger.info("Enumerated books")


    def zip_info_for_book(self, book_code):
        return self.zip.getinfo(book_code + '_metadata.xml')

    def zip_info_for_page(self, book_code, page):
        return self.zip.getinfo('ALTO/' + book_code + '_' + page + '.xml')

    def metadata_file(self, book_code):
        return self.zip.open(book_code + '_metadata.xml')

    def page_file(self, book_code, page):
        return self.zip.open('ALTO/' + book_code + '_' + page + '.xml')

    def __getitem__(self, index):
        self.logger.debug("Creating book")
        return Book(self.book_codes.keys()[index],self)

    def __iter__(self):
        for book in self.book_codes:
            self.logger.debug("Creating book")
            yield Book(book, self)

    def __len__(self):
        return len(self.book_codes)
