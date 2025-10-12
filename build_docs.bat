@echo off
REM Build script for Network Datasets documentation on Windows

echo Building Network Datasets Documentation
echo ======================================

REM Check if we're in the right directory
if not exist "ndtools" (
    echo Error: ndtools directory not found. Are you in the project root?
    exit /b 1
)

REM Install the package in development mode
echo Installing package in development mode...
pip install -e .
if errorlevel 1 (
    echo Failed to install package
    exit /b 1
)

REM Install documentation dependencies
echo Installing documentation dependencies...
pip install -r docs/requirements.txt
if errorlevel 1 (
    echo Failed to install documentation dependencies
    exit /b 1
)

REM Clean previous build
echo Cleaning previous build...
if exist "docs\_build" rmdir /s /q "docs\_build"

REM Build documentation
echo Building documentation...
cd docs
make.bat html
if errorlevel 1 (
    echo Failed to build documentation
    exit /b 1
)

echo.
echo Documentation built successfully!
echo Open docs\_build\html\index.html in your browser to view the documentation.

REM Check for warnings
echo.
echo Checking for documentation warnings...
sphinx-build -W -b html . _build/html
if errorlevel 1 (
    echo Warnings or errors found in documentation
) else (
    echo No warnings found in documentation
)

cd ..
