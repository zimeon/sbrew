from setuptools import setup, Command
import os
# setuptools used instead of distutils.core so that 
# dependencies can be handled automatically

class Coverage(Command):
    description = "run coverage"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("coverage run --source=sbrew setup.py test")
        os.system("coverage report")
        os.system("coverage html")
        print "See htmlcov/index.html for details."

setup(
    name='sbrew',
    version='0.0.1',
    packages=['sbrew'],
    scripts=[],
    classifiers=["Development Status :: 3 - Alpha",
                 "Operating System :: OS Independent", #is this true? know Linux & OS X ok
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2.7"],
    author='Simeon Warner',
    author_email='simeon.warner@cornell.edu',
    description='Simeon\'s Brewing Calculations',
    long_description=open('README.md').read(),
    url='http://github.com/zimeon/sbrew',
    install_requires=[],
    test_suite="tests",
    cmdclass={
        'coverage': Coverage,
    },
)
