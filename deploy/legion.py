from fabric.api import *
from mako.template import Template
import mako
import os
from datetime import datetime

env.run_at="/home/ucgajhe/Scratch/dataspring/output"
env.deploy_to="/home/ucgajhe/devel/dataspring"
env.clone_url="git@github.com:UCL/dataspring.git"
env.corpora="/home/ucgajhe/Scratch/dataspring"
env.hosts=['legion.rc.ucl.ac.uk']
env.user='ucgajhe'

@task
def cold(branch='master'):
    run('rm -rf '+env.deploy_to)
    run('mkdir -p '+env.deploy_to)
    run('mkdir -p '+env.run_at)
    with cd(env.deploy_to):
        with prefix('module swap compilers compilers/gnu/4.6.3'), \
             prefix('module swap mpi mpi/openmpi/1.6.5/gnu.4.6.3'),\
             prefix('module load python/2.7.3'),\
             prefix('module load rsd-modules'),\
             prefix('module load mpi4py'),\
             prefix('module load pyyaml'),\
             prefix('module load libxml'),\
             prefix('module load libxslt'),\
             prefix('module load lxml'),\
             prefix('module load userpython'):
                 run('git clone '+env.clone_url)
                 with cd('dataspring'):
                     run('git checkout '+branch)
                     run('python setup.py develop --user')
                     with prefix('module load pytest'):
                         run('py.test')

@task
def warm(branch='master'):
  with cd(os.path.join(env.deploy_to,'dataspring')):
        with prefix('module swap compilers compilers/gnu/4.6.3'),\
             prefix('module swap mpi mpi/openmpi/1.6.5/gnu.4.6.3'),\
             prefix('module load python/2.7.3'),\
             prefix('module load rsd-modules'),\
             prefix('module load mpi4py'),\
             prefix('module load pyyaml'),\
             prefix('module load libxml'),\
             prefix('module load libxslt'),\
             prefix('module load lxml'): 
                 run('echo $PYTHONPATH')
                 run('git checkout '+branch)
                 run('git pull')
                 run('python setup.py develop --user')



@task
def test(branch='master'):
  with cd(os.path.join(env.deploy_to,'dataspring')):
        with prefix('module swap compilers compilers/gnu/4.6.3'),\
             prefix('module swap mpi mpi/openmpi/1.6.5/gnu.4.6.3'),\
             prefix('module load python/2.7.3'),\
             prefix('module load rsd-modules'),\
             prefix('module load mpi4py'),\
             prefix('module load pyyaml'),\
             prefix('module load libxml'),\
             prefix('module load libxslt'),\
             prefix('module load lxml'): 
                 with prefix('module load pytest'):
                     run('py.test')

@task
def sub(query, corpus='CompressedALTO64',
        subsample=1, processes=4, wall='0:5:0',
        bybook=False):
    env.processes=processes
    env.subsample=subsample
    env.corpus=os.path.join(env.corpora,corpus)
    env.wall=wall
    now=datetime.now()
    stamp=now.strftime("%Y%m%d_%H%M")
    env.outpath=query+'_'+stamp
    if bybook:
        env.bybook="--bybook"
    else:
        env.bybook=""
    template_file_path=os.path.join(os.path.dirname(__file__),'legion.sh.mko')
    script_local_path=os.path.join(os.path.dirname(__file__),'legion.sh')
    config_file_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'queries',query+'.py')
    env.dest_query='query_'+stamp+'.py'
    with open(template_file_path) as template:
        script=Template(template.read()).render(**env)
        with open(script_local_path,'w') as script_file:
            script_file.write(script)
    with cd(env.run_at):
       put(config_file_path,env.dest_query)
       put(script_local_path,'query.sh')
       run('qsub query.sh')

@task
def repartition(inpath='CompressedALTO64',out='downsample_result',count=64,processes=1, wall='0:15:0', downsample=1):
    env.inpath=os.path.join(env.corpora,inpath)
    env.outpath=os.path.join(env.corpora,out)
    env.processes=processes
    env.wall=wall
    env.count=count
    env.downsample=downsample
    template_file_path=os.path.join(os.path.dirname(__file__),'repartition.sh.mko')
    script_local_path=os.path.join(os.path.dirname(__file__),'repartition.sh')
    with open(template_file_path) as template:
        script=Template(template.read()).render(**env)
        with open(script_local_path,'w') as script_file:
            script_file.write(script)
    with cd(env.run_at):
       put(script_local_path,'repartition.sh')
       run('qsub repartition.sh')
@task
def stat():
    run('qstat')

@task
def fetch():
    with lcd(os.path.join(os.path.dirname(os.path.dirname(__file__)),'results')):
      with cd(env.run_at):
        get('*')
