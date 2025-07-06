from distutils.core import setup

setup(
    name='perf_bench',
    author='Martin Privat',
    version='0.0.4',
    packages=['perf_bench'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='share numpy arrays between processes',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy", 
    ]
)