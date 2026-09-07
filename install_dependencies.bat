@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo Устанавливаю зависимости (Pillow, numpy)...
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
echo Похоже, что на компьютере не установлен настоящий Python
echo ^(если выше видно сообщение про Microsoft Store - это оно^).
echo.
echo Установите Python с https://www.python.org/downloads/
echo При установке ОБЯЗАТЕЛЬНО отметьте галочку "Add python.exe to PATH".
echo После установки закройте это окно и запустите install_dependencies.bat заново.
pause
exit /b 1

:found
echo Использую команду: %PYCMD%
"%PYCMD%" -m pip install --upgrade pip
"%PYCMD%" -m pip install pillow numpy
if errorlevel 1 goto :pip_failed

echo.
echo Готово. Теперь можно перетаскивать картинки на convert_normal.bat
pause
exit /b 0

:pip_failed
echo.
echo Установка библиотек не удалась - посмотрите текст ошибки выше.
pause
exit /b 1
