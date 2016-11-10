from fabric.api import *

@task
def grace():
    env.hosts=['grace.rc.ucl.ac.uk']
    env.machine='grace'
