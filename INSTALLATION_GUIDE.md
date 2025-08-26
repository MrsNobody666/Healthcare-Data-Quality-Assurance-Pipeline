# Healthcare Data Quality Assurance Pipeline - Installation Guide

## Quick Fix for Dependency Issues

Based on the terminal output, some packages in requirements.txt were causing installation failures. I've updated the requirements.txt file to use only available, compatible packages.

## Installation Steps

### 1. Clean Installation (Recommended)
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install updated requirements
pip install -r requirements.txt

# If any issues persist, install packages individually:
pip install pandas numpy pyyaml requests
pip install pydicom hl7apy python-dateutil
pip install pandera "great-expectations>=0.17.0" scipy
pip install scikit-learn statsmodels
pip install sqlalchemy psycopg2-binary
pip install matplotlib seaborn plotly
pip install python-dotenv loguru
pip install pytest pytest-cov
pip install sphinx sphinx-rtd-theme
pip install black flake8 mypy
pip install fastapi uvicorn
```

### 2. Alternative Installation Methods

#### Method A: Minimal Installation
```bash
# Install only essential packages
pip install pandas numpy pyyaml requests python-dateutil
```

#### Method B: Using conda
```bash
# Create conda environment
conda create -n healthcare-qa python=3.11
conda activate healthcare-qa

# Install packages
conda install pandas numpy scipy scikit-learn matplotlib seaborn
pip install pyyaml requests pydicom hl7apy pandera great-expectations
```

### 3. Verify Installation
```bash
# Test basic functionality
python -c "import pandas, numpy, yaml; print('Core packages installed successfully')"

# Run the demo
python main.py --demo
```

### 4. Common Issues and Solutions

#### Issue: psycopg2 installation fails
```bash
# On Windows, try:
pip install psycopg2-binary

# On Linux/macOS, if binary fails:
pip install psycopg2
```

#### Issue: pandera version conflicts
```bash
# Install compatible version
pip install "pandera>=0.15.0,<0.20.0"
```

#### Issue: great-expectations installation
```bash
# Install with specific version
pip install "great-expectations>=0.17.0,<1.0.0"
```

### 5. Development Setup

#### Install development dependencies
```bash
# Install development tools
pip install jupyter black flake8 mypy pytest pytest-cov

# Install pre-commit hooks (if available)
pip install pre-commit
pre-commit install
```

### 6. Environment Configuration

#### Create .env file (optional)
```bash
# Copy example environment
# cp .env.example .env

# Or create manually
echo "DATABASE_URL=postgresql://user:password@localhost/healthcare_qa" > .env
echo "LOG_LEVEL=INFO" >> .env
```

### 7. Test Installation

#### Run basic tests
```bash
# Run unit tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_data_validator.py -v

# Run demo
python main.py --demo
```

#### Check application health
```bash
# Validate configuration
python main.py --validate-config

# List available sources
python main.py --list-sources
```

## Platform-Specific Notes

### Windows
- Use PowerShell or Command Prompt
- Ensure Python is added to PATH
- Use `python` instead of `python3`

### macOS/Linux
- May need to use `python3` instead of `python`
- Install build tools: `xcode-select --install` (macOS)
- Install development packages: `sudo apt-get install python3-dev` (Ubuntu/Debian)

## Troubleshooting

### Error: "No module named 'src'"
```bash
# Ensure you're in the correct directory
cd healthcare-data-qa
python main.py --demo
```

### Error: Import errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Add current directory to Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

### Error: Permission denied
```bash
# On Unix systems, ensure permissions
chmod +x main.py
chmod +x run.bat
```

## Quick Start After Installation

```bash
# 1. Navigate to project directory
cd healthcare-data-qa

# 2. Activate virtual environment (if created)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Run the demo
python main.py --demo

# 4. Run batch processing example
python main.py --batch --config config_batch.yaml
```

## Support

If you continue to experience issues:
1. Check the [README.md](README.md) for detailed instructions
2. Review the [PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) for architecture details
3. Create an issue with the specific error message and system details