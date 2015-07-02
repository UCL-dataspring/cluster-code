import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bluclobber",
    version = "0.0.1",
    author = "James Hetherington",
    author_email = "j.hetherington@ucl.ac.uk",
    description = ("Harness for cluster map/reduce analysis of ALTO books corpus"),
    license = "BSD",
    keywords = "digital humanities research books",
    url = "http://development.rc.ucl.ac.uk/",
    packages=['bluclobber'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Research :: Humanities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
          'console_scripts': [
              'bluclobber = bluclobber.harness.query:main',
              'bluclobber_repartition = bluclobber.harness.repartition:main'
          ]
      },
)
