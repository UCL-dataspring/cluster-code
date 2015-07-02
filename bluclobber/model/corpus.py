import glob
import os
import traceback

from book import Book
from archive import Archive
from functools import reduce

from dataset import DataSet

from ..harness.mapreduce import MapReduce
from ..harness.utils import merge
from ..harness.decomposer import Decomposer

import logging

class Corpus(DataSet):
    def __init__(self, path=None, communicator=None):
        if type(path)==str:
            path+='/*.zip'
        super(Corpus, self).__init__(Archive,path,communicator )

    def analyse_by_book_in_archives(self, mapper, reducer, subsample=1, shuffler=None):
        partition=Corpus(Decomposer(self.paths, self.communicator))
        harness=MapReduce(self.loadingMap(mapper), reducer, self.communicator,
                prepartitioned=True, subsample=subsample, shuffler=shuffler )
        return harness.execute(partition)

    def analyse_by_book(self, mapper, reducer, subsample=1, shuffler=None):
        harness = MapReduce(self.loadingMap(mapper), reducer, self.communicator, subsample, shuffler=shuffler)
        return harness.execute(self)

    def analyse(self,mapper, reducer, subsample=1, bybook=False, shuffler=None):
        if bybook:
            self.logger.info("Analysing by book")
            return self.analyse_by_book_in_archives(mapper, reducer, subsample, shuffler)
        else:
            self.logger.info("Analysing by archive")
            return self.analyse_by_file(self.loadingMap(mapper), reducer, subsample, shuffler)

    def loadingMap(self, mapper):
        def _map(book):
            self.logger.debug("Loading book")
            try:
                book.load()
            except Exception as exception:
                self.logger.warn("Problem loading " + book.code + " in " + book.archive.path)
                self.logger.warn(traceback.format_exc())
                self.logger.warn(str(exception))
            self.logger.debug("Loaded book")
            try:
                self.logger.debug("Considering book")
                result= mapper(book)
                self.logger.debug("Considered book")
                return result
            except Exception as exception:
                self.logger.warn("Problem parsing " + book.code + " in " + book.archive.path)
                self.logger.warn(traceback.format_exc())
                self.logger.warn(str(exception))
        return _map
