from unittest import TestCase

import tempfile
import shutil
import os
import zipfile

import numpy as np
import glob

from mpi4py import MPI

from ...model.corpus import Corpus
from ...harness.repartition import repartition, repartition_from_metazip
from ..fixtures import path


class test_repartition(TestCase):
    def setUp(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.rank
        if self.rank==0:
            dest=tempfile.mkdtemp()
        else:
            dest=None
        self.dest=self.comm.bcast(dest)
        self.source=path('corpus24')
    def tearDown(self):
        pass
        #shutil.rmtree(self.dest)
    def test_repartition(self):
        repartition(self.source,self.dest,4)
        corpus=Corpus(self.dest)
        result = corpus.analyse(lambda x: np.array([1, x.pages]), lambda x,y: x+y)
        assert result.shape==(2,)
        assert result[0]==24
        assert result[1]==8364
    def test_repartition_metazip(self):
        meta=os.path.join(self.dest,'meta.zip')
        
        if self.rank==0:
            paths=glob.glob(os.path.join(self.source,'*.zip'))
            with zipfile.ZipFile(meta,'w') as metaz:
                for apath in paths:
                    metaz.write(apath,os.path.basename(apath))
        self.comm.Barrier()
        
        repartition_from_metazip(meta,self.dest,4)
        
        if self.rank==0:
            os.remove(meta)
        self.comm.Barrier()
        
        corpus=Corpus(self.dest)
        result = corpus.analyse(lambda x: np.array([1, x.pages]), lambda x,y: x+y)
        assert result.shape==(2,)
        assert result[0]==24
        assert result[1]==8364
    def test_repartition_downsample(self):
        repartition(self.source,self.dest,4,2)
        corpus=Corpus(self.dest)
        result = corpus.analyse(lambda x: np.array([1, x.pages]), lambda x,y: x+y)
        assert result.shape==(2,)
        assert result[0]==12
        assert result[1]==4044
