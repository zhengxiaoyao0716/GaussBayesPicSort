# -*- mode: python -*-

block_cipher = None


a = Analysis(['main-gui.py'],
             pathex=['E:\\MyProject\\Python\\pattern\\GaussBayesPicSort'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GaussBayesPicSort-gui',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='icon.ico')

# Copy  assets files
from shutil import rmtree, copytree
rmtree('./dist/assets/')
copytree('./assets/', './dist/assets/')