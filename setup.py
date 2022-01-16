from distutils.core import setup
from Cython.Build import cythonize

setup(name='seam_carve app',
      ext_modules=cythonize("_seam_carving.pyx"))
