"""
Main entry point for the Healthcare Data Quality Assurance Pipeline.

This script provides a command-line interface for running the complete
healthcare data processing pipeline.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pipeline import HealthcareDataPipeline
from src.utils.healthcare_utils import HealthcareUtils


def create_sample_data():
    """Create sample data for testing purposes."""
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    # Create sample healthcare data
    np.random.seed(42)
    n_records = 100
    
    data = {
        'patient_id': [f'P{i:03d}' for i in range(n_records)],
        'birth_date': [
            (datetime.now() - timedelta(days=np.random.randint(6570, 29200))).strftime('%Y-%m-%d')
            for _ in range(n_records)
        ],
        'gender': np.random.choice(['M', 'F', 'U'], n_records),
        'race': np.random.choice(['White', 'Black', 'Asian', 'Other'], n_records),
        'admission_date': [
            (datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime('%Y-%m-%d')
            for _ in range(n_records)
        ],
        'discharge_date': [
            (datetime.now() - timedelta(days=np.random.randint(-30, 365))).strftime('%Y-%m-%d')
            for _ in range(n_records)
        ],
        'primary_diagnosis': np.random.choice(['I25.10', 'J44.1', 'N18.6'], n_records),
        'length_of_stay': np.random.randint(1, 30, n_records),
        'total_charges': np.random.lognormal(9, 1.5, n_records),
        'systolic_bp': np.random.normal(120, 20, n_records)
    }
    
    df = pd.DataFrame(data)
    
    # Add some data quality issues
    df.loc[5:10, 'gender'] = None
    df.loc[15:20, 'admission_date'] = 'invalid-date'
    
    return df


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Healthcare Data Quality Assurance Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --source uci_heart --name heart_study
  python main.py --batch --config custom_config.yaml
  python main.py --demo --output demo_output
  python main.py --create-sample --output sample_data.csv
        """
    )
    
    parser.add_argument(
        '--config', 
        default='config.yaml',
        help='Configuration file path (default: config.yaml)'
    )
    
    parser.add_argument(
        '--source', 
        choices=['cdc', 'cms', 'fda', 'mimic', 'eicu', 'uci_heart'],
        help='Data source type to process'
    )
    
    parser.add_argument(
        '--name', 
        help='Dataset name for processing'
    )
    
    parser.add_argument(
        '--output', 
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--batch', 
        action='store_true',
        help='Run batch processing using batch configuration'
    )
    
    parser.add_argument(
        '--demo', 
        action='store_true',
        help='Run demonstration with sample data'
    )
    
    parser.add_argument(
        '--create-sample', 
        action='store_true',
        help='Create sample healthcare data for testing'
    )
    
    parser.add_argument(
        '--validate-config', 
        action='store_true',
        help='Validate configuration file'
    )
    
    parser.add_argument(
        '--list-sources', 
        action='store_true',
        help='List available data sources'
    )
    
    parser.add_argument(
        '--verbose', 
        '-v', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    if args.list_sources:
        print("Available Data Sources:")
        print("- cdc: CDC (Centers for Disease Control)")
        print("- cms: CMS (Centers for Medicare & Medicaid Services)")
        print("- fda: FDA (Food and Drug Administration)")
        print("- mimic: MIMIC-IV Clinical Database")
        print("- eicu: eICU Collaborative Research Database")
        print("- uci_heart: UCI Heart Disease Dataset")
        return
    
    if args.validate_config:
        try:
            from src.pipeline import HealthcareDataPipeline
            pipeline = HealthcareDataPipeline(args.config)
            print(f"✅ Configuration file '{args.config}' is valid")
            return
        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            sys.exit(1)
    
    if args.create_sample:
        print("Creating sample healthcare data...")
        sample_df = create_sample_data()
        
        output_file = Path(args.output) / (args.name or "sample_healthcare_data.csv")
        sample_df.to_csv(output_file, index=False)
        
        print(f"✅ Sample data created: {output_file}")
        print(f"   Records: {len(sample_df)}")
        print(f"   Columns: {list(sample_df.columns)}")
        return
    
    if args.demo:
        print("🚀 Running Healthcare Data QA Pipeline Demo")
        print("=" * 50)
        
        # Create sample data
        sample_df = create_sample_data()
        sample_file = Path(args.output) / "demo_data.csv"
        sample_df.to_csv(sample_file, index=False)
        
        print(f"📊 Created sample data: {len(sample_df)} records")
        
        # Initialize pipeline
        pipeline = HealthcareDataPipeline(args.config)
        
        # Run validation and cleaning
        print("🔍 Running validation...")
        validation_results = pipeline.validate_data(sample_df, "demo_dataset")
        
        print("🧹 Running data cleaning...")
        cleaning_config = {
            'clean_column_names': True,
            'handle_missing_values': {'enabled': True, 'strategy': 'auto'},
            'standardize_dates': {
                'enabled': True,
                'columns': ['birth_date', 'admission_date', 'discharge_date']
            },
            'remove_duplicates': {'enabled': True, 'method': 'exact'}
        }
        
        cleaned_df, cleaning_report, cleaning_summary = pipeline.clean_data(
            sample_df, cleaning_config
        )
        
        print("⚠️  Running risk assessment...")
        risk_results = pipeline.assess_risks(cleaned_df)
        
        # Save results
        cleaned_file = Path(args.output) / "demo_cleaned.csv"
        pipeline.save_results(cleaned_df, str(cleaned_file))
        
        report_file = Path(args.output) / "demo_report.json"
        results = {
            'validation': validation_results,
            'cleaning': {'summary': cleaning_summary},
            'risk_assessment': risk_results,
            'summary': {
                'dataset_name': 'demo_dataset',
                'total_records': len(cleaned_df),
                'processing_date': str(pd.Timestamp.now())
            }
        }
        pipeline.generate_report(results, str(report_file))
        
        # Display summary
        print("\n📋 Demo Results Summary:")
        print(f"   Original records: {cleaning_summary['records_before']}")
        print(f"   Cleaned records: {cleaning_summary['records_after']}")
        print(f"   Quality score: {validation_results.get('overall_score', 'N/A')}")
        print(f"   Total risks: {len(risk_results['risks'])}")
        print(f"   Critical risks: {risk_results['summary']['severity_distribution'].get('critical', 0)}")
        
        print(f"\n📁 Files created:")
        print(f"   Sample data: {sample_file}")
        print(f"   Cleaned data: {cleaned_file}")
        print(f"   Report: {report_file}")
        
        return
    
    if args.batch:
        print("🔄 Running batch processing...")
        
        # Load batch configuration
        import yaml
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
        
        batch_sources = config.get('batch_sources', [])
        if not batch_sources:
            print("❌ No batch sources configured in config.yaml")
            return
        
        pipeline = HealthcareDataPipeline(args.config)
        results = pipeline.batch_process_sources(batch_sources, args.output)
        
        print("\n📊 Batch Processing Results:")
        print(f"   Total sources: {results['summary']['total_sources']}")
        print(f"   Processed successfully: {results['summary']['processed_successfully']}")
        print(f"   Failed: {results['summary']['failed_processing']}")
        print(f"   Success rate: {results['summary']['success_rate']:.1%}")
        
        return
    
    if args.source and args.name:
        print(f"🚀 Processing {args.source} dataset: {args.name}")
        
        pipeline = HealthcareDataPipeline(args.config)
        
        # Build kwargs from remaining arguments
        kwargs = {}
        # Add any additional parameters here based on source type
        
        results = pipeline.run_pipeline(
            source_type=args.source,
            dataset_name=args.name,
            output_dir=args.output,
            **kwargs
        )
        
        print("\n✅ Processing completed!")
        print(f"   Dataset: {args.name}")
        print(f"   Records: {results['summary']['total_records']}")
        print(f"   Quality score: {results['validation']['overall_score']:.2f}")
        print(f"   Total risks: {len(results['risk_assessment']['risks'])}")
        print(f"   Output directory: {args.output}")
        
    else:
        parser.print_help()
        print("\n💡 Try: python main.py --demo")


if __name__ == "__main__":
    main()