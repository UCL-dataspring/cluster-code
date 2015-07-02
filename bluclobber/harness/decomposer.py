import logging
from itertools import islice

class Decomposer(object):
    def __init__(self, iterable, communicator=None, rank=None, size=None, subsample=1, offsets=None):
        logger=logging.getLogger('performance')
        self.logger=logger
        if not size:
            if not communicator:
                logger.debug("Assuming default rank and size")
                rank=0
                size=1
            else:
                logger.debug("Rank and size from MPI communicator")
                rank=communicator.rank
                size=communicator.size
        self.iterable=iterable
        if not offsets:
            self.count=len(iterable)/size
            if rank==size-1:
                self.remainder=len(iterable)%size
            else:
                self.remainder=0
            self.start=self.count*rank
            self.end=self.count*(rank+1)+self.remainder
            self.step=subsample
            self.step_offset=self.start%self.step
            logger.debug("Splitting " +str(len(iterable))+ " items into " + str(size) + " chunks of " + str(self.count))
            logger.debug("This is chunk " + str(rank) + " from " +str(self.start) + " to " + str(self.end))

    def __str__(self):
        return "Decomposer of len " + str(len(self)) + " from " +str(self.start)  + " to " + str(self.end) + " in steps " + str(self.step)

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError
        new_index=self.start+index*self.step+self.step_offset
        return self.iterable[new_index]

    def __len__(self):
        return (self.end-1)/self.step-(self.start-1)/self.step
