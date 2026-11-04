@echo off
rem Builds "MMBN3 - Perfect Version.gba" and release\MMBN3-Perfect.bps.
rem Needs: armips.exe (in PATH or this folder); Python 3 with numpy, Pillow, scipy.
cd /d "%~dp0"
python tools\make_title.py || echo (title logo step skipped - vanilla title will be used)
armips main.asm || goto :error
python tools\make_bps.py || goto :error
echo Done.
goto :eof
:error
echo Build failed.
exit /b 1
