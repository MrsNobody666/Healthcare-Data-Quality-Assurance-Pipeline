# Healthcare Data Quality Assurance Pipeline

A comprehensive Python toolkit for collecting, validating, cleaning, and assessing the quality of healthcare datasets from various sources including government databases, clinical datasets, and research repositories.

## 🏥 Overview

This project provides a complete solution for healthcare data quality assurance, featuring:

- **Data Collection**: Automated collection from CDC, CMS, FDA, MIMIC-IV, eICU, and academic datasets
- **Data Validation**: Comprehensive validation against healthcare data quality standards
- **Data Cleaning**: Automated cleaning and standardization of healthcare data
- **Risk Assessment**: Advanced risk detection and mitigation strategies
- **Quality Metrics**: Detailed quality scoring and reporting
- **Privacy Protection**: Built-in privacy risk assessment and anonymization

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Data Sources](#data-sources)
- [Quality Framework](#quality-framework)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Install from Source

```bash
# Clone the repository
git clone https://github.com/your-org/healthcare-data-qa.git
cd healthcare-data-qa

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Install via pip (when available)

```bash
pip install healthcare-data-qa
```

## 🎯 Quick Start

### Basic Usage

```python
from src.pipeline import HealthcareDataPipeline

# Initialize pipeline
pipeline = HealthcareDataPipeline("config.yaml")

# Process a single dataset
results = pipeline.run_pipeline(
    source_type="uci_heart",
    dataset_name="heart_disease_study",
    output_dir="output"
)

print(f"Processed {results['summary']['total_records']} records")
print(f"Quality score: {results['validation']['overall_score']:.2f}")
print(f"Risks identified: {len(results['risk_assessment']['risks'])}")
```

### Batch Processing

```python
# Process multiple sources
sources = [
    {"type": "cdc", "name": "mortality_data", "params": {"year": 2022}},
    {"type": "cms", "name": "medicare_claims", "params": {"state": "CA"}},
    {"type": "uci_heart", "name": "heart_study"}
]

batch_results = pipeline.batch_process_sources(sources, "output")
print(f"Processed {batch_results['summary']['processed_successfully']} sources")
```

## 🏗️ Architecture

### Project Structure

```
healthcare-data-qa/
├── src/
│   ├── data_collection/     # Data source collectors
│   ├── data_validation/     # Validation rules and checks
│   ├── quality_assurance/   # Data cleaning and standardization
│   ├── risk_assessment/     # Risk detection and mitigation
│   ├── utils/              # Healthcare-specific utilities
│   └── pipeline.py         # Main orchestration
├── config/                 # Configuration files
├── examples/               # Usage examples
├── tests/                 # Unit tests
├── docs/                  # Documentation
└── output/                # Generated outputs
```

### Core Components

1. **Data Collectors**: Specialized collectors for different data sources
2. **Validator**: Comprehensive data quality validation
3. **Cleaner**: Automated data cleaning and standardization
4. **Risk Engine**: Advanced risk assessment and mitigation
5. **Pipeline**: Main orchestration and workflow management

## 📊 Data Sources

### Supported Sources

| Source | Type | Description | Collector |
|--------|------|-------------|-----------|
| **CDC** | Government | Centers for Disease Control datasets | `CDCDataCollector` |
| **CMS** | Government | Medicare/Medicaid datasets | `CMSDataCollector` |
| **FDA** | Government | Food and Drug Administration data | `FDADataCollector` |
| **MIMIC-IV** | Clinical | ICU clinical database | `MIMICDataCollector` |
| **eICU** | Clinical | eICU Collaborative Research Database | `eICUDataCollector` |
| **UCI Heart** | Academic | Heart disease study dataset | `UCIHeartDiseaseCollector` |

### Adding New Sources

Create a new collector by extending `BaseDataCollector`:

```python
from src.data_collection.collectors import BaseDataCollector

class CustomDataCollector(BaseDataCollector):
    def collect(self, **kwargs):
        # Implementation for your data source
        pass
```

## ⚙️ Configuration

### Configuration File (config.yaml)

```yaml
# Data Sources Configuration
data_sources:
  cdc:
    api_key: "your_api_key"
    base_url: "https://data.cdc.gov"
    timeout: 30
  
  cms:
    api_key: "your_api_key"
    base_url: "https://data.cms.gov"
    
  mimic:
    data_dir: "./data/mimic"
    physionet_username: "your_username"

# Validation Parameters
validation:
  completeness_threshold: 0.95
  accuracy_threshold: 0.90
  consistency_threshold: 0.85
  
# Cleaning Configuration
cleaning:
  handle_missing_values:
    enabled: true
    strategy: "auto"
  standardize_dates:
    enabled: true
    format: "%Y-%m-%d"
  remove_duplicates:
    enabled: true
    method: "exact"

# Risk Assessment
risk_assessment:
  critical_columns:
    - patient_id
    - birth_date
    - primary_diagnosis
  risk_thresholds:
    missing_data:
      critical: 0.5
      high: 0.3
      medium: 0.1
    
# Logging
logging:
  level: "INFO"
  file: "healthcare_data_pipeline.log"
```

## 🔍 Quality Framework

### Quality Dimensions

The framework evaluates data quality across six key dimensions:

1. **Accuracy**: Correctness of data values
2. **Completeness**: Presence of required data
3. **Consistency**: Uniformity across datasets
4. **Timeliness**: Currency and freshness of data
5. **Validity**: Conformance to defined formats
6. **Uniqueness**: Absence of duplicate records

### Validation Rules

#### Healthcare-Specific Validations

- **ICD-10 Code Validation**: Ensures valid diagnosis and procedure codes
- **Date Consistency**: Validates temporal relationships (admission < discharge)
- **Clinical Ranges**: Checks vital signs and lab values against normal ranges
- **Patient Demographics**: Validates age, gender, and other demographic data
- **Insurance Codes**: Validates insurance type classifications

#### Statistical Validations

- **Outlier Detection**: Identifies extreme values using statistical methods
- **Distribution Analysis**: Monitors data drift and anomalies
- **Completeness Analysis**: Tracks missing data patterns
- **Duplicate Detection**: Identifies and handles duplicate records

### Risk Assessment

#### Risk Categories

- **Missing Critical Data**: Essential fields with missing values
- **Invalid Medical Codes**: Incorrect ICD, CPT, or other medical codes
- **Temporal Anomalies**: Impossible date relationships
- **Outlier Values**: Extreme values requiring clinical review
- **Privacy Risks**: Potential HIPAA violations
- **Data Drift**: Changes in data distributions over time

#### Risk Levels

- **Critical**: Immediate attention required
- **High**: Significant impact on analysis
- **Medium**: Moderate impact, should be addressed
- **Low**: Minor issues, can be documented
- **Info**: Informational only

## 📈 Usage Examples

### Example 1: Processing CDC Mortality Data

```python
# Process CDC mortality data for 2022
results = pipeline.run_pipeline(
    source_type="cdc",
    dataset_name="mortality_2022",
    output_dir="./output/cdc",
    params={
        "dataset": "mortality",
        "year": 2022,
        "state": "CA"
    }
)

print(f"CDC data processed: {results['summary']['total_records']} records")
print(f"Quality score: {results['validation']['overall_score']:.2f}")
```

### Example 2: Custom Validation Rules

```python
from src.data_validation.validator import DataValidator

# Create custom validator
validator = DataValidator({
    "completeness_threshold": 0.98,
    "accuracy_threshold": 0.95,
    "custom_rules": {
        "systolic_bp": {
            "min": 70,
            "max": 300,
            "type": "numeric"
        },
        "discharge_date": {
            "after": "admission_date"
        }
    }
})

# Run validation
results = validator.run_comprehensive_validation(df)
```

### Example 3: Risk Assessment

```python
from src.risk_assessment.risk_manager import RiskAssessmentEngine

# Initialize risk engine
risk_engine = RiskAssessmentEngine({
    "critical_columns": ["patient_id", "birth_date", "diagnosis"],
    "risk_thresholds": {
        "missing_data": {"critical": 0.05, "high": 0.02}
    }
})

# Run risk assessment
risk_results = risk_engine.run_comprehensive_risk_assessment(df)

# Generate report
report = risk_engine.generate_risk_report(risk_results['risks'])
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_validator.py

# Run with coverage
pytest --cov=src tests/
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end pipeline testing
- **Validation Tests**: Healthcare-specific validation rules
- **Performance Tests**: Large dataset processing

## 📊 Output Formats

### Generated Files

- **Cleaned Data**: CSV, Parquet, or JSON formats
- **Validation Reports**: JSON format with detailed metrics
- **Risk Reports**: JSON format with risk assessment
- **Processing Logs**: Detailed execution logs
- **Quality Metrics**: Summary statistics

### Report Structure

```json
{
  "pipeline_metadata": {
    "execution_date": "2024-01-15T10:30:00",
    "dataset_name": "heart_disease_study",
    "source_type": "uci_heart"
  },
  "processing_summary": {
    "original_records": 1000,
    "cleaned_records": 950,
    "quality_score": 0.92,
    "total_risks": 15
  },
  "validation_results": {
    "completeness": 0.95,
    "accuracy": 0.98,
    "consistency": 0.94
  },
  "risk_assessment": {
    "critical_risks": 2,
    "high_risks": 5,
    "medium_risks": 8
  }
}
```

## 🔧 Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run linting
flake8 src/

# Run type checking
mypy src/
```

### Contributing Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-feature`)
3. **Commit** changes (`git commit -am 'Add new feature'`)
4. **Push** to branch (`git push origin feature/new-feature`)
5. **Create** a Pull Request

### Code Standards

- **PEP 8** compliance
- **Type hints** for all functions
- **Docstrings** for all classes and methods
- **Unit tests** for new features
- **Integration tests** for pipeline changes

## 📚 Documentation

### API Documentation

Generate API documentation:

```bash
# Install documentation dependencies
pip install -r requirements-docs.txt

# Generate documentation
cd docs/
make html
```

### Available Documentation

- **User Guide**: Comprehensive usage instructions
- **API Reference**: Detailed API documentation
- **Examples**: Real-world usage examples
- **Architecture**: Technical architecture overview

## 🛡️ Security and Privacy

### Privacy Protection

- **HIPAA Compliance**: Built-in privacy risk assessment
- **Data Anonymization**: Automatic PII detection and removal
- **Access Control**: Configurable data access restrictions
- **Audit Trail**: Complete processing logs

### Security Features

- **Input Validation**: SQL injection prevention
- **File Validation**: Malicious file detection
- **Rate Limiting**: API request throttling
- **Encryption**: Optional data encryption at rest

## 🚀 Performance

### Optimization Features

- **Parallel Processing**: Multi-threaded data processing
- **Memory Management**: Efficient handling of large datasets
- **Caching**: Configurable result caching
- **Progress Monitoring**: Real-time processing status

### Benchmarks

| Dataset Size | Processing Time | Memory Usage |
|-------------|----------------|--------------|
| 10K records | ~2 minutes     | ~500 MB      |
| 100K records| ~15 minutes    | ~2 GB        |
| 1M records  | ~2 hours       | ~8 GB        |

## 🔄 Troubleshooting

### Common Issues

#### Import Errors
```python
# Ensure package is installed
pip install -e .

# Check Python path
import sys
print(sys.path)
```

#### Configuration Errors
```bash
# Validate configuration
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

#### Memory Issues
```python
# Process in chunks
pipeline.run_pipeline(..., chunk_size=10000)
```

### Support

- **Issues**: [GitHub Issues](https://github.com/your-org/healthcare-data-qa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/healthcare-data-qa/discussions)
- **Documentation**: [Full Documentation](https://healthcare-data-qa.readthedocs.io)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CDC**: For providing public health datasets
- **CMS**: For Medicare and Medicaid data
- **PhysioNet**: For MIMIC-IV and eICU databases
- **UCI Machine Learning Repository**: For heart disease dataset
- **Healthcare Data Scientists**: Community feedback and contributions

## 📞 Contact

- **Project Maintainer**: Healthcare Data QA Team
- **Email**: healthcare-data-qa@example.com
- **Slack**: [#healthcare-data-qa](https://slack.com/channels/healthcare-data-qa)
- **Twitter**: [@healthcare_data_qa](https://twitter.com/healthcare_data_qa)

---

**Made with ❤️ for better healthcare data quality**