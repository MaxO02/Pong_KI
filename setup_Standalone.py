import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tk8.6"

executables = [cx_Freeze.Executable("__init__.py")]

cx_Freeze.setup(
    name="Pong_clone",
    options = {
        "build_exe":{
            "packages":["pygame","multitasking","configparser"],
            "include_files": ["Pong","Pong/config.cfg","Pong/soundfiles"]
        }
    },
    executables = executables
)



