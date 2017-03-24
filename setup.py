#!/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""
GaussBayesPicSort
@author: zhengxiaoyao0716
"""

import sys
import os
import distutils
from shutil import rmtree, copytree

from cx_Freeze import setup, Executable

# Copy assets files
out_assets_dir = './build/exe.%s-%s/assets/' % \
    (distutils.util.get_platform(), sys.version[0:3])
rmtree(out_assets_dir, ignore_errors=True)
copytree('./assets/', out_assets_dir)

# Repair tkinter lib
PYTHON3_HOME = os.environ['PYTHON3']
os.environ['TCL_LIBRARY'] = PYTHON3_HOME + "\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = PYTHON3_HOME + "\\tcl\\tk8.6"

name = 'GaussBayesPicSort'
name_gui = 'GaussBayesPicSort-gui'
if sys.platform == 'win32':
    suffix = '.exe'
    base_gui = "Win32GUI"
else:
    suffix = ''
    base_gui = "Console"

setup(name=name,
      version='1.0',
      description='GaussBayesPicSort',
      options={'build_exe': {
          'includes': [
              'numpy.core._methods',
              'numpy.lib.format',
              'matplotlib.backends.backend_tkagg',
              'tkinter.filedialog',
          ],
          'include_files': [
              '.env/Lib/site-packages/mpl_toolkits',
              PYTHON3_HOME + '/DLLs/tcl86t.dll',
              PYTHON3_HOME + '/DLLs/tk86t.dll',
          ],
      }},
      executables=[
          Executable('main.py', base=None,
                     targetName=name + suffix, icon="icon.ico",),
          Executable('main-gui.py', base=base_gui,
                     targetName=name_gui + suffix, icon="icon.ico",)
      ])
