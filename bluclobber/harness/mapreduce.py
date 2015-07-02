from functools import reduce
from mpi4py import MPI
from itertools import islice
from datetime import datetime as time
import logging
from collections import defaultdict

from decomposer import Decomposer

class MapReduce(object):
    def __init__(self, mapper, reducer,  communicator=None, subsample=1, shuffler=None, prepartitioned=False ):
        self.unsafe_mapper = mapper
        self.unsafe_reducer = reducer
        self.unsafe_shuffler = shuffler
        self.subsample = subsample
        self.communicator=communicator
        self.prepartitioned=prepartitioned
        self.logger=logging.getLogger('performance')
        # safe reduce
        def safeReducer(a, b):
            if a is None:
                return b
            if b is None:
                return a
            return self.unsafe_reducer(a,b)
        self.reducer=safeReducer
        # safe map
        def safeMap(arg):
            self.logger.debug("Entered mapper")
            try:
                result= self.unsafe_mapper(arg)
                self.logger.debug("Exiting mapper")
                return result
            except Exception as e:
                self.logger.warn("Problem with map")
                self.logger.warn(str(e))
                return None
        self.mapper=safeMap
        if shuffler:
            def safeShuffler(arg, count):
                try:
                    return self.unsafe_shuffler(arg, count)
                except Exception as e:
                    self.logger.warn("Problem with shuffle")
                    self.logger.warn(str(e))
                    return None
            self.shuffler=safeShuffler
        else:
            self.shuffler=None

    def execute(self, data):
        if self.communicator and self.communicator.size>1:
            return self.parallel(data)
        else:
            return self.serial(data)

    def serial(self, data):
        try:
            count=len(data)
        except AttributeError:
            count=None
        subsampled_data=Decomposer(data, subsample=self.subsample)
        quantities= map(self.mapper, subsampled_data)
        result = reduce(self.reducer, quantities)
        return result

    def parallel(self, data):
        perfLogger=logging.getLogger('performance')
        # local map
        if self.prepartitioned:
            partition=Decomposer(data,subsample=self.subsample)
        else:
            partition=Decomposer(data, self.communicator, subsample=self.subsample )
        perfLogger.info("Built iterator")
        quantities=map(self.mapper,partition)
        perfLogger.info("Mapped")
        local_result=reduce(self.reducer, quantities)
        perfLogger.info("Local reduce")
        # reduce under mpi
        def reduce_arrays(x,y,dtype):
            # the signature for the user defined op takes a datatype, which we can ignore
            return self.reducer(x,y)
        reducer_mpi=MPI.Op.Create(reduce_arrays, True)
        perfLogger.debug("Local result: "+str(local_result)[0:60])
        if self.shuffler:
            perfLogger.info("Shuffling")
            shuffled=defaultdict(dict)
            if local_result:
                for key in local_result:
                    shuffled[self.shuffler(key, self.communicator.size)][key]=local_result[key]
            for root in range(self.communicator.size):
                perfLogger.info("Reducing to rank "+str(root))
                temp=self.communicator.reduce(shuffled[root],op=reducer_mpi,root=root)
                if self.communicator.rank==root:
                    result=temp
        else:
            result = self.communicator.reduce(local_result, op=reducer_mpi, root=0)
            result = self.communicator.bcast(result, root=0)
        perfLogger.info("Global reduce")
        
        reducer_mpi.Free()
        return result
