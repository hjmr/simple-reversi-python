from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("stone", ["stone.pyx"]),
    Extension("board", ["board.pyx"]),
    Extension("evaluator", ["evaluator.pyx"]),
]

setup(
    name="reversi",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
)
