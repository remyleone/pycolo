# -*- coding:utf-8 -*-

from distutils.core import setup
import pycolo

setup(
    name='pycolo',
    version=pycolo.__version__,
    description='Python CoAP lightweight Operator.',
    author='Rémy Léone',
    license=open('LICENCE').read(),
    author_email='remy.leone@gmail.com',
    long_description='%s\n\n' % open('README.md').read(),
    url="http://pycolo.sieben.fr",
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        )
)
