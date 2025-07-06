from distutils.core import setup

setup(
    name='perf_bench',
    author='Martin Privat',
    version='0.1.0',
    packages=['perf_bench'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='share numpy arrays between processes',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy", 
    ]
)