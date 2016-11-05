from setuptools import setup, find_packages

setup(
    name='aioleakybucket',
    version='0.1a',
    author='Konstantin Ignatov',
    author_email='kv@qrator.net',
    packages=find_packages(exclude='tests'),
    install_requires=[
        'heapdict',
    ],
)
