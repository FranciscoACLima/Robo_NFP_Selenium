import os
from cx_Freeze import setup, Executable

DIR_BASE = os.path.dirname(__file__)

local_files = [
    os.path.join(DIR_BASE, "nfp", "controle_execucao.db"),
    os.path.join(DIR_BASE, "nfp", "config_maquina.json"),
    os.path.join(DIR_BASE, "nfp", "config_window.json")
]
for file in local_files:
    if os.path.isfile(file):
        os.unlink(file)

build_exe_options = {
    "packages": [
        "sqlalchemy"
    ],
    "includes": [],
    "include_files": [],
    "excludes": [
        'nfp.prefs_chrome',
        'nfp.binaries'
    ],
    "bin_excludes": [],
    "optimize": 1,
    "build_exe": "build/RoboNFP"
}

base = None

setup(
    name="RoboNFP",
    version="0.1.0",
    description="Robô para cadastro de Nota Fiscal Paulista",
    options={"build_exe": build_exe_options},
    executables=[Executable("run.py", base=base, target_name='RoboNFP', icon="ico.ico")])
