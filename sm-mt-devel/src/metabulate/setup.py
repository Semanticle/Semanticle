#!/usr/bin/python
from distutils.core import setup
setup(name='Metabulate',
      version='1.64',
      description='Semanticle Distributed Inferencing Triple Store',
      author='Anthony Machin',
      author_email='tm@semanticle.org',
      url='http://www.semanticle.org',
      packages=['metabulate'
               ,'metabulate.stores'
               ,'metabulate.facades'
               ,'metabulate.utils'
               ,'metabulate.renderers'
               ,'metabulate.rules'
               ,'metabulate.singletons'
               ,'metabulate.parsers'
               ,'metabulate.queries'
               ,'metabulate.tests'],
     )
