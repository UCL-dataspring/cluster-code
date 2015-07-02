from ...harness.mapreduce import MapReduce
import numpy as np
from mpi4py import MPI
import logging
from ...harness.utils import *

perfLogger=logging.getLogger('performance')
communicator=MPI.COMM_WORLD
perfLogger.setLevel(logging.DEBUG)
stdout=logging.StreamHandler()
stdout.setFormatter(logging.Formatter(str(communicator.rank)+'/'+str(communicator.size)+
    ' %(levelname)s: %(asctime)s %(message)s'))
perfLogger.addHandler(stdout)

def test_sum_squares_serial():
    data = np.arange(12)
    mapper = lambda x: x*x
    reducer = lambda x,y: x+y
    harness=MapReduce(mapper, reducer, None)
    assert(harness.execute(data)==0+1+4+9+16+25+36+49+64+81+100+121)

def test_ignore_nones_serial():
    data = range(12)
    data.append(None)
    mapper = lambda x: x*x
    reducer = lambda x,y: x+y
    harness=MapReduce(mapper, reducer, None)
    assert(harness.execute(data)==0+1+4+9+16+25+36+49+64+81+100+121)

def test_sum_squares_parallel():
    data = np.arange(12)
    mapper = lambda x: x*x
    reducer = lambda x,y: x+y
    communicator=MPI.COMM_WORLD
    harness=MapReduce(mapper, reducer, communicator)
    result= harness.execute(data)
    assert (result==0+1+4+9+16+25+36+49+64+81+100+121)

def test_sum_squares_remainder():
    data = np.arange(7)
    mapper = lambda x: x*x
    reducer = lambda x,y: x+y
    communicator=MPI.COMM_WORLD
    harness=MapReduce(mapper, reducer, communicator)
    result= harness.execute(data)
    assert (result==0+1+4+9+16+25+36)

def test_subsample_serial():
    data = np.arange(12)
    mapper = lambda x: x*x
    reducer = lambda x,y: x+y
    harness=MapReduce(mapper, reducer,None,2)
    assert(harness.execute(data)==0+4+16+36+64+100)

def test_sum_squares_parallel_downsample():
    data = np.arange(12)
    mapper = lambda x: x*x
    reducer = lambda x,y: x+y
    communicator=MPI.COMM_WORLD
    harness=MapReduce(mapper, reducer,communicator, 2)
    result= harness.execute(data)
    assert (result==0+4+16+36+64+100)

def test_shuffled():
    data = np.arange(24)
    mapper = lambda x: {x%8: x*x}
    reducer = merge_under(add)
    shuffler = lambda key, size: key%size 
    communicator=MPI.COMM_WORLD
    if communicator.size != 4:
        return
    harness=MapReduce(mapper, reducer,communicator,shuffler=shuffler)
    result= harness.execute(data)
    if communicator.rank==0:
        assert result=={0: 8*8+16*16, 4: 4*4+12*12+20*20}



