import os
from cx_Freeze import setup, Executable

DIR_BASE = os.path.dirname(__file__)

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "sqlalchemy"
    ],
    "includes": [],
    "include_files": [],
    "excludes": [
        'nfp.prefs_chrome'
    ],
    "bin_excludes": ['config.py'],
    "optimize": 1
}

base = None

setup(
    name="RoboNFP",
    version="0.0.4",
    description="Robô para cadastro de Nota Fiscal Paulista",
    options={"build_exe": build_exe_options},
    executables=[Executable("run.py", base=base, target_name='RoboNFP', icon="ico.ico")])
