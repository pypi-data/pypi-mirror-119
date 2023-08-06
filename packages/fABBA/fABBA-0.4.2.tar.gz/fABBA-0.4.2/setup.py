import setuptools
from pathlib import Path
from Cython.Build import cythonize
import numpy

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="fABBA",
    packages=setuptools.find_packages(),
    version="0.4.2",
    setup_requires=["cython", "numpy", "scipy"],
    install_requires=["numpy"],
    ext_modules=cythonize(["fABBA/*.pyx"], include_path=["fABBA"]),
    include_dirs=[numpy.get_include()],
    long_description=long_description,
    author="Stefan Guettel, Xinye Chen",
    author_email="stefan.guettel@manchester.ac.uk",
    description="An efficient aggregation based symbolic representation",
    long_description_content_type='text/markdown',
    url="https://github.com/nla-group/fABBA",
    license='BSD 3-Clause'
)
