from ..fixtures import mean_pages as sample_query
from ..fixtures import path

from ...harness.query import query, clparser

def test_query():
    source=path('corpus24')
    from mpi4py import MPI
    result=query(sample_query.mapper, sample_query.reducer, source) 
    if MPI.COMM_WORLD.rank==0:
        assert result == [24,8364]
    else:
        assert result == None

def test_parser_simple():
    space=clparser(['abc','def'])
    assert space.corpus_path=='def'
    assert space.query_path=='abc'
    assert space.downsample==1

def test_parser_downsample():
    space=clparser(['abc','def','--downsample','4'])
    assert space.corpus_path=='def'
    assert space.query_path=='abc'
    assert space.downsample==4

