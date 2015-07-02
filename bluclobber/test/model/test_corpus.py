from unittest import TestCase

from ...model.corpus import Corpus
from ..fixtures import path

import numpy as np

class test_corpus(TestCase):
    def setUp(self):
        from mpi4py import MPI
        self.communicator=MPI.COMM_WORLD
        self.source=path('corpus24')
        self.corpus=Corpus(self.source,self.communicator)
    def test_glob(self):
        assert(len(self.corpus)==24)
    def test_downsample(self):
        result = self.corpus.analyse(lambda x: np.array([1, x.pages]),
                lambda x,y: x+y, 2, bybook=True)
        assert result.shape==(2,)
        assert result[0]==12
    def test_analyse_by_book(self):
        result = self.corpus.analyse(
                lambda x: np.array([1, x.pages]), lambda x,y: x+y, bybook=True )
        assert result.shape==(2,)
        assert result[0]==24
        assert result[1]==8364
    def test_analyse(self):
        result = self.corpus.analyse(lambda x: np.array([1, x.pages]), lambda x,y: x+y)
        assert result.shape==(2,)
        assert result[0]==24
        assert result[1]==8364
