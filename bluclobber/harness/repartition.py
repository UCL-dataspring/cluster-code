import os
import zipfile
import sys
from argparse import ArgumentParser
from itertools import islice
import shutil
import tempfile
import subprocess
import logging
from mpi4py import MPI
import glob
from ..model.corpus import Corpus
from decomposer import Decomposer

def main():
    perfLogger=logging.getLogger('performance')
    communicator=MPI.COMM_WORLD
    perfLogger.setLevel(logging.DEBUG)
    stdout=logging.StreamHandler()
    stdout.setFormatter(logging.Formatter(str(communicator.rank)+'/'+str(communicator.size)+
        ' %(levelname)s: %(asctime)s %(message)s'))
    perfLogger.addHandler(stdout)
    args = parser(sys.argv[1:])
    # verify outpath exists or create if not
    try:
        os.makedirs(args.out_path)
    except os.error:
        pass # Folder exists, nicer in Python 3
    # restripe if Lustre striping given
    if args.stripe:
        subprocess.check_call(['lfs','setstripe','--count', args.stripe, args.out_path])
    if '.zip' in args.in_path:
        repartition_from_metazip(args.in_path,args.out_path,args.split)
    else:
        repartition(args.in_path,args.out_path,args.split, args.downsample)

def parser(commandline):
    parser=ArgumentParser(description="Repartition a corpus")
    parser.add_argument('in_path',type=str, help='path to corpus to repartition')
    parser.add_argument('out_path',type=str, help='path to folder to contain repartitioned corpus')
    parser.add_argument('--downsample',type=int, metavar='N', default=1, help='optionally, use only every Nth book')
    parser.add_argument('--split',type=int, metavar='N', default=64, help='repartition to N zipfiles')
    parser.add_argument('--stripe',type=int, metavar='N', default=None, help='Lustre striping for output')
    args=parser.parse_args(commandline)
    return args

def repartition(in_path, out_path, split, downsample=1, filter=lambda x: True):
    perfLogger=logging.getLogger('performance')
    corpus=Corpus(in_path, communicator=MPI.COMM_WORLD)
    this_processor_out=Decomposer(range(split), communicator=MPI.COMM_WORLD)
    processor_paths=Decomposer(corpus.paths, communicator=MPI.COMM_WORLD)
    processor_corpus=Corpus(processor_paths)
    for chunk_index, chunk in enumerate(this_processor_out):
        perfLogger.info("Starting output zip "+str(chunk)) 
        books=Decomposer(processor_corpus, rank=chunk_index, size=len(this_processor_out), subsample=downsample )
        perfLogger.debug("Will handle "+str(len(books)) +" books.")
        with zipfile.ZipFile(os.path.join(out_path,'chunk'+str(chunk)+'.zip'),'w',allowZip64=True) as outzip:
            for book in books:
                book.load()
                if not filter(book):
                    continue
                info=book.zip_info()
                # transfer from small zip to bigger zip
                outzip.writestr(info, book.archive.zip.read(info))
                for page_code in book.page_codes:
                    info=book.page_zip_info(page_code)
                    outzip.writestr(info, book.archive.zip.read(info))
        perfLogger.info("Completed output zip " +str(chunk))
    MPI.COMM_WORLD.Barrier()

def repartition_from_metazip(in_zip, out_path, split):
    tmpdir=tempfile.mkdtemp()
    this_processor=Decomposer(range(split))
    with zipfile.ZipFile(in_zip) as metazip:
        inzips=metazip.infolist()
        for chunk in this_processor:
            # open a zip for writing
            with zipfile.ZipFile(os.path.join(out_path,'chunk'+str(chunk)+'.zip'),'w',allowZip64=True) as outzip:
                this_chunk=list(islice(metazip.infolist(),chunk,None,split))
                for archive in this_chunk:
                    # open a smaller zip
                    metazip.extract(archive,tmpdir)
                    small=os.path.join(tmpdir,archive.filename)
                    # should be able to do this in memory, but
                    # zipfile doesn't like importing from file-like-object
                    try:
                        with zipfile.ZipFile(small) as inzip:
                        # transfer from small zip to bigger zip
                            for info in inzip.infolist():
                                outzip.writestr(info, inzip.read(info))
                    except zipfile.BadZipfile:
                        print "Bad file:", archive.filename
                    os.remove(small)
    shutil.rmtree(tmpdir)
    MPI.COMM_WORLD.Barrier()



