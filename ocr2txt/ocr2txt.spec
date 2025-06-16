# ocr2txt.spec
block_cipher = None

a = Analysis(
    ['ocr2txt.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('tesseract/tesseract.exe', 'tesseract'),
        ('tesseract/tessdata/eng.traineddata', 'tesseract/tessdata'),
        ('tesseract/tessdata/por.traineddata', 'tesseract/tessdata'),
    ],
    hiddenimports=['pdf2image', 'pytesseract', 'PIL.Image', 'PIL.ImageFilter', 'PIL.ImageOps'],
    hookspath=[],
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
    name='ocr2txt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Coloque o caminho do .ico aqui se quiser
)
