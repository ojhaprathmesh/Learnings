from cx_Freeze import setup, Executable

exe_options = {"packages": ["pygame","random", "os","sys", "pkg_resources.py2_warn"]}

setup(name="Snakes By Prathmesh",
      version="1.1.0",
      description="My Python Game",
      options={"build_exe": exe_options},
      executables=[Executable("Snakes.py", base="Win32GUI")]
      )