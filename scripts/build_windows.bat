@echo off
setlocal

cd /d "%~dp0\.."

for /f "usebackq delims=" %%i in (`python -c "from pdf2office.metadata import APP_ID; print(APP_ID)"`) do set "APP_ID=%%i"
for /f "usebackq delims=" %%i in (`python -c "from pdf2office.metadata import APP_VERSION; print(APP_VERSION)"`) do set "APP_VERSION=%%i"
for /f "usebackq delims=" %%i in (`python -c "from pdf2office.metadata import APP_BUILD_BY; print(APP_BUILD_BY)"`) do set "APP_BUILD_BY=%%i"

echo [1/3] Installing build dependencies...
python -m pip install -r requirements-build.txt
if errorlevel 1 goto :error

echo [2/3] Building %APP_ID% v%APP_VERSION% (build by %APP_BUILD_BY%)...
python -m PyInstaller --noconfirm pdf2office.spec
if errorlevel 1 goto :error

echo [3/3] Build complete.
echo Output: dist\%APP_ID%\%APP_ID%.exe
exit /b 0

:error
echo Build failed.
exit /b 1
