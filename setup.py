#!/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""
GaussBayesPicSort
@author: zhengxiaoyao0716
"""

import sys
import os

from cx_Freeze import setup, Executable

PYTHON3_HOME = os.environ['PYTHON3']
os.environ['TCL_LIBRARY'] = PYTHON3_HOME + "\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = PYTHON3_HOME + "\\tcl\\tk8.6"

name = 'GaussBayesPicSort'
base = "Console"

if sys.platform == 'win32':
    name = name + '.exe'
    # base = "Win32GUI"

setup(name='main',
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
          ]
      }},
      executables=[Executable(
          'main.py', base=base, targetName=name, icon="icon.ico",
      )])
