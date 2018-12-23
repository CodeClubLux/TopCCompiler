import os

dir = os.getcwd()

os.chdir(dir + "/TopCompiler/TopRuntime")
from importlib import util
spec = util.spec_from_file_location("runtimebuild.py", dir + "/bin/runtimebuild.py")
foo = util.module_from_spec(spec)
spec.loader.exec_module(foo)

os.chdir(dir)

from setuptools import setup

setup(name='TopCCompiler',
      version='0.1',
      description='Compiler for Top programming language',
      url='https://github.com/CodeClubLux/TopCCompiler',
      author='CompilerLuke',
      author_email="lgoetz@islux.lu",
      scripts= ["bin/topc", "bin/topdev", "bin/port.py", "bin/port", "bin/topr", "bin/topc.py", "bin/topr.py", "bin/topdev.py"],
      license='MIT',
      zip_safe=False,
      packages= ["TopCompiler","AST", "optimization","PostProcessing"],
      install_requires=[],
      include_package_data=True
)