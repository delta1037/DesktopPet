# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['desktop_pet.py'],
    pathex=[
        'desktop_pet/__init__.py',
        'desktop_pet/chat_openai.py',
        'desktop_pet/param_db.py',
        'desktop_pet/pet_theme.py',
        'desktop_pet/ui_pet_chat.py',
    ],
    binaries=[],
    datas=[('./theme', './theme/.'),],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    [],
    exclude_binaries=True,
    name='desktop_pet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='desktop_pet',
)
