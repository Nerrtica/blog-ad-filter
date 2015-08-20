
try :
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
    
#from distutils import msvc9compiler
from Cython.Build import cythonize

#msvc9compiler.VERSION = 8.0

setup(
    name='crawling lib',
    ext_modules = cythonize('*.pyx')
)
