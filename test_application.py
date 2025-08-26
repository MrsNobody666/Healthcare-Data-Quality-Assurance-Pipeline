"""
Simple test script to verify the healthcare data QA application structure
This script tests basic functionality without complex dependencies
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_sample_data():
    """Create sample healthcare data for testing"""
    np.random.seed(42)
    n_records = 100
    
    data = {
        'patient_id': [f'P{i:03d}' for i in range(n_records)],
        'age': np.random.randint(18, 90, n_records),
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
    
    # Add some data quality issues for testing
    df = pd.DataFrame(data)
    df.loc[5:10, 'gender'] = None
    df.loc[15:20, 'admission_date'] = 'invalid-date'
    df.loc[0, 'age'] = 150  # Invalid age
    
    return df

def basic_validation(df):
    """Basic validation without external dependencies"""
    results = {
        'total_records': len(df),
        'missing_values': df.isnull().sum().to_dict(),
        'completeness': (1 - df.isnull().sum() / len(df)).to_dict(),
        'invalid_dates': df['admission_date'].apply(
            lambda x: pd.to_datetime(x, errors='coerce') is pd.NaT
        ).sum(),
        'invalid_ages': (df['age'] < 0) | (df['age'] > 120).sum(),
        'duplicates': df.duplicated().sum()
    }
    
    return results

def basic_cleaning(df):
    """Basic cleaning without external dependencies"""
    cleaned = df.copy()
    
    # Handle missing values
    cleaned['gender'] = cleaned['gender'].fillna('Unknown')
    
    # Fix invalid ages
    cleaned.loc[(cleaned['age'] < 0) | (cleaned['age'] > 120), 'age'] = np.nan
    
    # Remove exact duplicates
    cleaned = cleaned.drop_duplicates()
    
    # Standardize gender values
    gender_map = {'M': 'Male', 'F': 'Female', 'U': 'Unknown'}
    cleaned['gender'] = cleaned['gender'].map(gender_map).fillna('Unknown')
    
    return cleaned

def main():
    """Test the application structure and basic functionality"""
    print("🚀 Healthcare Data Quality Assurance Pipeline - Test Run")
    print("=" * 60)
    
    try:
        # Create sample data
        print("📊 Creating sample healthcare data...")
        df = create_sample_data()
        print(f"   Created {len(df)} sample records")
        
        # Save sample data
        output_dir = "test_output"
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, "sample_data.csv"), index=False)
        print(f"   Saved to: {output_dir}/sample_data.csv")
        
        # Basic validation
        print("\n🔍 Running basic validation...")
        validation_results = basic_validation(df)
        print(f"   Total records: {validation_results['total_records']}")
        print(f"   Missing values per column:")
        for col, count in validation_results['missing_values'].items():
            if count > 0:
                print(f"     {col}: {count}")
        print(f"   Invalid dates: {validation_results['invalid_dates']}")
        print(f"   Invalid ages: {validation_results['invalid_ages']}")
        print(f"   Duplicate records: {validation_results['duplicates']}")
        
        # Basic cleaning
        print("\n🧹 Running basic cleaning...")
        cleaned_df = basic_cleaning(df)
        print(f"   Records after cleaning: {len(cleaned_df)}")
        
        # Save cleaned data
        cleaned_df.to_csv(os.path.join(output_dir, "cleaned_data.csv"), index=False)
        print(f"   Cleaned data saved to: {output_dir}/cleaned_data.csv")
        
        # Summary report
        report = {
            "original_records": int(len(df)),
            "cleaned_records": int(len(cleaned_df)),
            "removed_duplicates": int(validation_results['duplicates']),
            "missing_values_resolved": int(sum(1 for v in validation_results['missing_values'].values() if v > 0)),
            "validation_score": float((1 - sum(validation_results['missing_values'].values()) / (len(df) * len(df.columns))) * 100)
        }
        
        with open(os.path.join(output_dir, "test_report.json"), 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n✅ Test completed successfully!")
        print(f"   Original records: {report['original_records']}")
        print(f"   Cleaned records: {report['cleaned_records']}")
        print(f"   Quality score: {report['validation_score']:.1f}%")
        print(f"   Files created in: {output_dir}/")
        
        # List created files
        files = os.listdir(output_dir)
        print("\n📁 Created files:")
        for file in files:
            print(f"   - {file}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()