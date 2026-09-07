@echo off
rem То же самое, что convert_normal.bat, но с инвертированным зелёным каналом (Y).
rem Используйте, если после обычной конвертации нормали выглядят "вывернутыми".
setlocal enabledelayedexpansion
chcp 65001 >nul

set "SCRIPT_DIR=%~dp0"
set "PY_SCRIPT=%SCRIPT_DIR%unity_normal_unswizzle.py"

if not exist "%PY_SCRIPT%" (
    echo Не найден файл unity_normal_unswizzle.py рядом с этим bat-файлом.
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
echo Похоже, что на компьютере не установлен настоящий Python
echo ^(если выше видно сообщение про Microsoft Store - это оно^).
echo.
echo Установите Python с https://www.python.org/downloads/
echo При установке ОБЯЗАТЕЛЬНО отметьте галочку "Add python.exe to PATH".
echo После установки запустите install_dependencies.bat.
pause
exit /b 1

:found
if "%~1"=="" (
    echo Перетащите на этот файл картинку ^(.dds, .png, .tga...^) - можно сразу несколько.
    pause
    exit /b 0
)

:loop
if "%~1"=="" goto :done

set "IN=%~1"
set "OUTDIR=%~dp1"
set "OUT=%OUTDIR%%~n1_normal.png"

echo ------------------------------------------------------------
echo Конвертирую (invert-y): %IN%
"%PYCMD%" "%PY_SCRIPT%" "%IN%" "%OUT%" --invert-y
if errorlevel 1 (
    echo [ОШИБКА] Не удалось сконвертировать: %IN%
) else (
    echo Готово: %OUT%
)

shift
goto :loop

:done
echo ------------------------------------------------------------
echo Все файлы обработаны.
pause
