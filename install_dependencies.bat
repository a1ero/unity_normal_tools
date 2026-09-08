@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo I’m installing the dependencies (Pillow, numpy)...
echo.

set "PYCMD=py"
py -c "print(1)" >nul 2>nul
if errorlevel 1 goto :try_python
goto :found

:try_python
set "PYCMD=python"
python -c "print(1)" >nul 2>nul
if errorlevel 1 goto :not_found
goto :found

:not_found
echo.
echo It seems that the computer doesn’t have the real Python installed
echo ^(If you see a message about the Microsoft Store above, that’s it^).
echo.
echo Install Python from https://www.python.org/downloads/
echo During installation, be sure to check the box “Add python.exe to PATH”.
echo After installation, close this window and run install_dependencies.bat again.
pause
exit /b 1

:found
echo I’m using the command: %PYCMD%
"%PYCMD%" -m pip install --upgrade pip
"%PYCMD%" -m pip install pillow numpy
if errorlevel 1 goto :pip_failed

echo.
echo Done. Now you can drag images onto convert_normal.bat
pause
exit /b 0

:pip_failed
echo.
echo The library installation failed — please review the error text above.
pause
exit /b 1
