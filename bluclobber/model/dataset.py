import glob
import os
import traceback

from functools import reduce
from ..harness.mapreduce import MapReduce
from ..harness.utils import merge
from ..harness.decomposer import Decomposer

import logging

class DataSet(object):
    def __init__(self, parser, path=None, communicator=None):
        self.logger=logging.getLogger('performance')
        try:
            self.paths=glob.glob(path)
        except AttributeError:
            self.paths=path
        self.parser=parser
        self.communicator=communicator
        self.files={}
        self.lengths=None

    def count(self):
        if self.lengths:
            return
        self.logger.debug("Counting contents")
        harness=MapReduce(lambda x: {x: len(self.get_file(x))}, merge, self.communicator)
        self.lengths= harness.execute(self.paths)
        self.logger.debug("Counted "+ str(len(self)) +" items")

    def __getitem__(self, index):
        self.count()
        self.logger.debug("Finding file for index "+ str(index))
        for path in self.paths:
            length=self.lengths[path]
            if index<length:
                self.logger.debug("Found in "+ path)
                return self.get_file(path)[index]
            else:
                index-=length
        raise IndexError()

    def __len__(self):
        self.count()
        return sum(self.lengths.values())

    def get_file(self, path):
        if path not in self.files:
            self.logger.debug("Creating file "+ path)
            self.files[path]=self.parser(path)
        return self.files[path]

    def get_file_by_index(self, index):
        return self.get_file(self.paths[index])

    def pathMap(self, mapper, reducer, subsample):
        def _map(path):
            archive=self.get_file(path)
            # Serial mapreduce for all items in the dataset
            harness=MapReduce(mapper, reducer, None, subsample)
            return harness.execute(archive)
        return _map

    def analyse_by_file(self, mapper, reducer, subsample=1, shuffler=None):
        harness=MapReduce(self.pathMap(mapper, reducer, subsample), reducer, self.communicator, shuffler=shuffler)
        return harness.execute(self.paths)
