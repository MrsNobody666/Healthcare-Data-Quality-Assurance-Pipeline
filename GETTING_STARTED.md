# Healthcare Data Quality Assurance Pipeline - Getting Started

## 🎯 What This Application Does

This is a comprehensive **Healthcare Data Quality Assurance Pipeline** that automates the process of collecting, validating, cleaning, and assessing healthcare data quality. It handles multiple data sources, identifies quality issues, and provides actionable recommendations.

## 🏗️ Application Architecture

### Core Components
1. **Data Collection Layer** - Collects from CDC, CMS, FDA, MIMIC, eICU, UCI datasets
2. **Validation Engine** - Checks completeness, accuracy, consistency, timeliness, uniqueness
3. **Data Cleaning** - Handles missing values, duplicates, standardization, normalization
4. **Risk Assessment** - Identifies data quality risks and provides mitigation strategies
5. **Reporting System** - Generates comprehensive quality reports

### Directory Structure
```
healthcare-data-qa/
├── src/                    # Main application code
│   ├── __init__.py        # Package initialization
│   ├── pipeline.py        # Main pipeline orchestrator
│   ├── risk_assessment/   # Risk management module
│   └── utils/            # Healthcare utilities
├── tests/                # Unit tests
├── examples/             # Usage examples
├── docs/                 # Documentation
├── config.yaml          # Configuration file
├── config_batch.yaml    # Batch processing config
├── main.py             # CLI entry point
└── run.bat            # Windows batch script
```

## 🚀 Quick Start

### 1. Installation
```bash
# Basic installation
pip install pandas numpy pyyaml requests python-dateutil

# For full functionality
pip install -r requirements.txt

# If requirements.txt fails, use individual packages
pip install pandas numpy scipy scikit-learn matplotlib seaborn
pip install pyyaml requests pydicom hl7apy pandera
```

### 2. Test the Application
```bash
# Run the test script (works with basic dependencies)
python test_application.py

# Expected output:
# ✅ 100 sample records created
# ✅ Quality score: 99.4%
# ✅ Files created in test_output/
```

### 3. Run the Full Pipeline
```bash
# Create sample data
python main.py --create-sample --output sample_data

# Run demo mode
python main.py --demo

# Batch processing
python main.py --batch --config config_batch.yaml

# List available data sources
python main.py --list-sources
```

### 4. Using the Windows Batch Script
```bash
# Run demo
run.bat demo

# Run tests
run.bat test

# Batch processing
run.bat batch

# Show help
run.bat help
```

## 📊 Data Sources Supported

### Government Sources
- **CDC** - Centers for Disease Control datasets
- **CMS** - Centers for Medicare & Medicaid Services
- **FDA** - Food and Drug Administration data

### Clinical Datasets
- **MIMIC** - Medical Information Mart for Intensive Care
- **eICU** - eICU Collaborative Research Database
- **UCI Heart Disease** - University of California Irvine dataset

### Custom Data
- CSV files
- JSON data
- Database connections (PostgreSQL)

## 🔍 Quality Checks Performed

### 1. Completeness
- Missing value detection
- Required field validation
- Data availability assessment

### 2. Accuracy
- Data type validation
- Range checking (age, dates, measurements)
- ICD-10 code validation
- Clinical measurement validation

### 3. Consistency
- Cross-field validation
- Logical relationships
- Temporal consistency

### 4. Timeliness
- Data freshness checks
- Outdated record identification
- Update frequency assessment

### 5. Uniqueness
- Duplicate detection
- Primary key validation
- Patient ID uniqueness

## 🧹 Data Cleaning Features

### Missing Data Handling
- **Drop**: Remove records with missing values
- **Fill**: Replace with mean, median, mode, or custom values
- **Forward Fill**: Use previous values
- **Interpolation**: Linear interpolation for time series

### Standardization
- **Gender**: Standardizes M/F/U to Male/Female/Unknown
- **Race**: Standardizes race/ethnicity codes
- **Insurance**: Standardizes insurance type codes
- **Dates**: Flexible date format parsing

### Data Quality Fixes
- **Duplicates**: Exact and fuzzy duplicate removal
- **Outliers**: Statistical outlier detection and handling
- **Invalid Codes**: ICD-10, CPT, HCPCS code validation
- **Measurement Units**: Standardization of units

## 📈 Output Files

### Generated Reports
- `validation_report.json` - Detailed validation results
- `cleaning_report.json` - Cleaning actions taken
- `risk_assessment.json` - Quality risks identified
- `summary_report.html` - Visual summary report

### Processed Data
- `cleaned_data.csv` - Cleaned dataset
- `missing_data.csv` - Records with missing values
- `invalid_data.csv` - Records with validation errors
- `duplicate_data.csv` - Duplicate records

## 🎯 Use Cases

### 1. Healthcare Research
- Validate research datasets
- Ensure data quality for clinical studies
- Identify bias in data collection

### 2. Hospital Analytics
- Clean EMR/EHR data
- Validate patient records
- Generate quality metrics

### 3. Insurance Analytics
- Validate claims data
- Identify fraudulent patterns
- Ensure compliance data quality

### 4. Public Health
- Monitor disease surveillance data
- Validate health survey responses
- Assess population health data quality

## 🔧 Configuration

### Basic Configuration
```yaml
# config.yaml
quality_thresholds:
  completeness: 0.95
  accuracy: 0.90
  consistency: 0.85

data_sources:
  cdc:
    enabled: true
    api_key: your_api_key
  
  cms:
    enabled: true
    dataset: medicare_claims
```

### Batch Processing
```yaml
# config_batch.yaml
batch_settings:
  sources: ["cdc", "cms", "mimic"]
  output_dir: "./batch_results"
  max_records: 10000
```

## 📋 Testing

### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_data_validator.py

# Run with coverage
python -m pytest tests/ --cov=src
```

### Manual Testing
```bash
# Create test data
python test_application.py

# Check output files in test_output/
```

## 🚨 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure you're in the project directory
2. **Missing Dependencies**: Install using pip install -r requirements.txt
3. **Memory Issues**: Reduce batch size in config files
4. **Permission Errors**: Run as administrator on Windows

### Quick Fixes
```bash
# Reset Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"

# Check Python version (3.8+ required)
python --version

# Verify dependencies
python -c "import pandas; print('Pandas:', pandas.__version__)"
```

## 📞 Support

### Documentation
- [README.md](README.md) - Complete project documentation
- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Installation instructions
- [PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) - Technical architecture

### Getting Help
1. Check the test_output/ folder after running `test_application.py`
2. Review the generated reports for data quality insights
3. Use the batch script (`run.bat`) for common operations
4. Examine the configuration files for customization options

## 🎉 Success Indicators

You'll know the application is working correctly when:
- ✅ `test_application.py` runs without errors
- ✅ Files appear in `test_output/` directory
- ✅ Quality score is displayed (typically 90%+)
- ✅ Generated CSV files contain cleaned data
- ✅ JSON reports contain detailed quality metrics

The application is now **ready for production use** with your healthcare data quality assurance needs!