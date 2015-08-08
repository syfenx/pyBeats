from cx_Freeze import setup,Executable

includefiles = ['coders_crux.ttf', 'bass.dll', 'project.txt']

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], 'include_files':includefiles}

setup(
    name = 'pyBeats',
    version = '0.5',
    description = 'python beat sequencer',
    author = 'Sam - syfenx@gmail.com',
    options = {"build_exe": build_exe_options}, 
	executables = [Executable(script="pyBeats.py", base="Win32GUI", targetName="pyBeats.exe")]
)
