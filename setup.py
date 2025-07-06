from distutils.core import setup

setup(
    name='PerfBench',
    author='Martin Privat',
    version='0.0.1',
    packages=['benchmarks'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='share numpy arrays between processes',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy", 
    ]
)