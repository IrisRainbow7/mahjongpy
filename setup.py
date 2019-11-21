from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'mahjongpy',
    packages = ['mahjongpy'],
    version = '0.1.4',
    license = 'MIT',
    install_requires = [],
    author = 'Irisrainbow7',
    author_email = '',
    url = 'https://github.com/Irisrainbow7/mahjongpy',
    description = 'Japanese-style mahjong library for python',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = 'mahjongpy mahjong',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 4 - Beta',
        'Natural Language :: Japanese',
        ],
    )
