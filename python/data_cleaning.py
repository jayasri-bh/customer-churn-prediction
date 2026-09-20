import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        
    def load_data(self):
        """Load CSV file"""
        self.df = pd.read_csv(self.filepath)
        print(f"✅ Data loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        return self.df
    
    def explore_data(self):
        """Basic data exploration"""
        print("\n📊 Dataset Info:")
        print(self.df.info())
        print("\n📈 First few rows:")
        print(self.df.head())
        print("\n📉 Missing values:")
        print(self.df.isnull().sum())
        
    def clean_data(self):
        """Clean the data"""
        # Remove duplicates
        self.df = self.df.drop_duplicates()
        print(f"✅ Duplicates removed")
        
        # Handle missing values
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
        print(f"✅ Missing values handled")
        
        # Remove unnecessary columns (adjust based on your dataset)
        cols_to_drop = ['customerID'] if 'customerID' in self.df.columns else []
        self.df = self.df.drop(columns=cols_to_drop, errors='ignore')
        print(f"✅ Unnecessary columns removed")
        
        return self.df
    
    def encode_categorical(self):
        """Encode categorical variables"""
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        le_dict = {}
        
        for col in categorical_cols:
            le = LabelEncoder()
            self.df[col] = le.fit_transform(self.df[col].astype(str))
            le_dict[col] = le
            
        print(f"✅ {len(categorical_cols)} categorical columns encoded")
        return self.df, le_dict
    
    def save_cleaned_data(self, output_path):
        """Save cleaned data"""
        self.df.to_csv(output_path, index=False)
        print(f"✅ Cleaned data saved to: {output_path}")
        
    def get_summary(self):
        """Get data summary"""
        summary = {
            'rows': self.df.shape[0],
            'columns': self.df.shape[1],
            'missing_values': self.df.isnull().sum().sum(),
            'duplicates': self.df.duplicated().sum()
        }
        return summary

# Main execution
if __name__ == "__main__":
    # Define paths - UPDATE THESE TO MATCH YOUR DATASET NAME
    input_path = "data/Telco_customer_churn.csv"  # Change to your actual CSV filename
    output_path = "data/cleaned_data.csv"
    
    # Process data
    processor = DataProcessor(input_path)
    processor.load_data()
    processor.explore_data()
    processor.clean_data()
    processor.encode_categorical()
    processor.save_cleaned_data(output_path)
    
    print("\n✅ Data cleaning completed!")
    print(processor.get_summary())