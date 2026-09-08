@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

set "SCRIPT_DIR=%~dp0"
set "PY_SCRIPT=%SCRIPT_DIR%unity_normal_unswizzle.py"

if not exist "%PY_SCRIPT%" (
    echo The file unity_normal_unswizzle.py was not found next to this bat file.
    echo Place both files in the same folder.
    pause
    exit /b 1
)

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
echo ^(If you see a message about the Microsoft Store above, that’s it.^).
echo.
echo Install Python from https://www.python.org/downloads/
echo During installation, be sure to check the box “Add python.exe to PATH”.
echo After installation, run install_dependencies.bat.
pause
exit /b 1

:found
if "%~1"=="" (
    echo Drag the image onto this file. ^(.dds, .png, .tga...^) - you can have several at once.
    pause
    exit /b 0
)

:loop
if "%~1"=="" goto :done

set "IN=%~1"
set "OUTDIR=%~dp1"
set "OUT=%OUTDIR%%~n1_normal.png"

echo ------------------------------------------------------------
echo I’m converting: %IN%
"%PYCMD%" "%PY_SCRIPT%" "%IN%" "%OUT%"
if errorlevel 1 (
    echo [ERROR] Failed to convert: %IN%
) else (
    echo Done: %OUT%
)

shift
goto :loop

:done
echo ------------------------------------------------------------
echo All files have been processed.
pause
