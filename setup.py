from setuptools import setup
# setuptools used instead of distutils.core so that 
# dependencies can be handled automatically

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
    long_description=open('README.rst').read(),
    url='http://github.com/zimeon/sbrew',
    install_requires=[],
    test_suite="tests",
)
