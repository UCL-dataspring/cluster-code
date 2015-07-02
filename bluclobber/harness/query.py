from ..model.corpus import Corpus
from ..model.dataset import DataSet
from mpi4py import MPI
import imp
import sys
from datetime import datetime
from argparse import ArgumentParser
import logging
import yaml
from utils import * 

shuffler=None
reporter=None
parser=Corpus

def main():
    args = clparser(sys.argv[1:])
    execfile(args.query_path, globals()) # must define 'mapper' and 'reducer'
                                         # may define shuffler and reporter
    perfLogger=logging.getLogger('performance')
    communicator=MPI.COMM_WORLD
    perfLogger.setLevel(getattr(logging,args.loglevel.upper()))
    stdout=logging.StreamHandler()
    stdout.setFormatter(logging.Formatter(str(communicator.rank)+'/'+str(communicator.size)+
        ' %(levelname)s: %(asctime)s %(message)s'))
    perfLogger.addHandler(stdout)
    result = query(mapper, reducer, args.corpus_path, args.downsample, args.bybook,
                   parser=parser, shuffler=shuffler, reporter=reporter)
    outpath=args.outpath+'_'+str(MPI.COMM_WORLD.rank)+'.yml'
    if result:
        if args.outpath:
            with open(outpath,'w') as result_file:
                result_file.write(yaml.safe_dump(result))
                perfLogger.info("Written result")
        else:
            print result

def clparser(commandline):
    clparser=ArgumentParser(description="Analyse a corpus")
    clparser.add_argument('query_path',type=str, help='path to python file describing query')
    clparser.add_argument('corpus_path',type=str, help='path to folder containing zipped corpus')
    clparser.add_argument('--downsample',type=int, metavar='N', default=1, help='optionally, use only every Nth zipfile')
    clparser.add_argument('--bybook', action="store_true", default=False)
    clparser.add_argument('--outpath', default=None, type=str, help = 'output path to yaml dump result')
    clparser.add_argument('--loglevel', default='info', type=str, help = 'log level (debug, info, warn, error)')
    args=clparser.parse_args(commandline)
    return args

def query(mapper, reducer, corpus_path, downsample=1, bybook=False, parser=parser, shuffler=None, reporter=None):
    communicator=MPI.COMM_WORLD
    perfLogger=logging.getLogger('performance')
    if parser==Corpus:
        corpus=Corpus(corpus_path,communicator)
        perfLogger.info("Constructed")
        result = corpus.analyse(mapper, reducer, downsample, bybook, shuffler=shuffler)
    else:
        corpus=DataSet(parser, corpus_path, communicator)
        result = corpus.analyse_by_file(mapper, reducer, downsample, shuffler=shuffler  )
    perfLogger.info("Finished analysis")
    if (not shuffler) and communicator.rank !=0:
        result=None
    if reporter and result:
           result=reporter(result)
           perfLogger.info("Finished postprocessing")
    return result

if __name__ == "__main__":
    main()
