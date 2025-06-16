# pdf_manipulation.spec
# Gera um .exe sem console, com arquivos adicionais incluídos
# Desenvolvido para Gustavo de Tarso

block_cipher = None

a = Analysis(
    ['pdf_manipulation.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('bin/qpdf.exe', 'bin'),
        ('bin/gswin64c.exe', 'bin'),
    ],
    hiddenimports=[],
    hookspath=[],
    # hooksconfig={},  # Removido para compatibilidade
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pdf_manipulation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # importante: sem console
    disable_windowed_traceback=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='appicon.ico',
)
