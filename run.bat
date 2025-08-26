@echo off
echo Healthcare Data Quality Assurance Pipeline
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your system PATH
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

REM Set default configuration
set CONFIG=config.yaml
set OUTPUT=output

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :main
if "%~1"=="--help" goto :help
if "%~1"=="-h" goto :help
if "%~1"=="--demo" (
    echo Running demonstration...
    python main.py --demo --output demo_output
    pause
    exit /b 0
)
if "%~1"=="--test" (
    echo Running tests...
    python -m pytest tests/ -v
    pause
    exit /b 0
)
if "%~1"=="--batch" (
    echo Running batch processing...
    python main.py --batch --config config_batch.yaml
    pause
    exit /b 0
)
if "%~1"=="--create-sample" (
    echo Creating sample data...
    python main.py --create-sample --output sample_data
    pause
    exit /b 0
)
shift
goto :parse_args

:main
echo Available commands:
echo   --demo        Run demonstration with sample data
echo   --test        Run all unit tests
echo   --batch       Run batch processing with multiple sources
echo   --create-sample Create sample healthcare data
echo   --help        Show this help message
echo.
echo Or use: python main.py [options]
echo.
echo Press any key to exit...
pause
exit /b 0

:help
echo Usage: run.bat [OPTIONS]
echo.
echo Options:
echo   --demo          Run demonstration with sample healthcare data
echo   --test          Run comprehensive unit tests
echo   --batch         Process multiple data sources in batch
echo   --create-sample Generate sample data for testing
echo   --help          Show this help message
echo.
echo Examples:
echo   run.bat --demo
echo   run.bat --test
echo   run.bat --batch
echo   python main.py --source uci_heart --name heart_study
echo   python main.py --list-sources
pause
exit /b 0