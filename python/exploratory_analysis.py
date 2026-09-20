import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class ExploratoryAnalysis:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.output_dir = "Images"
        sns.set_style("whitegrid")
        
    def churn_distribution(self):
        """Churn distribution"""
        fig, ax = plt.subplots(figsize=(8, 5))
        churn_counts = self.df['Churn Label'].value_counts()
        colors = ['#2ecc71', '#e74c3c']
        churn_counts.plot(kind='bar', color=colors, ax=ax)
        ax.set_title('Customer Churn Distribution', fontsize=14, fontweight='bold')
        ax.set_ylabel('Count')
        ax.set_xlabel('Churn Status')
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/01_churn_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Churn distribution saved")
        
    def tenure_vs_churn(self):
        """Tenure vs Churn"""
        fig, ax = plt.subplots(figsize=(10, 5))
        self.df.groupby('Tenure Months')['Churn Value'].mean().plot(ax=ax, color='#3498db', linewidth=2)
        ax.set_title('Churn Rate by Tenure', fontsize=14, fontweight='bold')
        ax.set_ylabel('Churn Rate')
        ax.set_xlabel('Tenure (Months)')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/02_tenure_vs_churn.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Tenure vs Churn saved")
        
    def monthly_charges_vs_churn(self):
        """Monthly charges vs Churn"""
        fig, ax = plt.subplots(figsize=(10, 5))
        churn_no = self.df[self.df['Churn Value'] == 0]['Monthly Charges']
        churn_yes = self.df[self.df['Churn Value'] == 1]['Monthly Charges']
        
        ax.hist([churn_no, churn_yes], bins=30, label=['No Churn', 'Churn'], color=['#2ecc71', '#e74c3c'])
        ax.set_title('Monthly Charges Distribution by Churn', fontsize=14, fontweight='bold')
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Monthly Charges ($)')
        ax.legend()
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/03_monthly_charges_vs_churn.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Monthly charges vs Churn saved")
        
    def contract_type_analysis(self):
        """Contract type analysis"""
        fig, ax = plt.subplots(figsize=(10, 5))
        contract_churn = pd.crosstab(self.df['Contract'], self.df['Churn Label'], normalize='index') * 100
        contract_churn.plot(kind='bar', color=['#2ecc71', '#e74c3c'], ax=ax)
        ax.set_title('Churn Rate by Contract Type', fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentage (%)')
        ax.set_xlabel('Contract Type')
        plt.xticks(rotation=45)
        plt.legend(title='Churn')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/04_contract_type_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Contract type analysis saved")
        
    def internet_service_analysis(self):
        """Internet service analysis"""
        fig, ax = plt.subplots(figsize=(10, 5))
        internet_churn = pd.crosstab(self.df['Internet Service'], self.df['Churn Label'], normalize='index') * 100
        internet_churn.plot(kind='bar', color=['#2ecc71', '#e74c3c'], ax=ax)
        ax.set_title('Churn Rate by Internet Service Type', fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentage (%)')
        ax.set_xlabel('Internet Service')
        plt.xticks(rotation=45)
        plt.legend(title='Churn')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/05_internet_service_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Internet service analysis saved")
        
    def gender_analysis(self):
        """Gender analysis"""
        fig, ax = plt.subplots(figsize=(8, 5))
        gender_churn = pd.crosstab(self.df['Gender'], self.df['Churn Label'], normalize='index') * 100
        gender_churn.plot(kind='bar', color=['#2ecc71', '#e74c3c'], ax=ax)
        ax.set_title('Churn Rate by Gender', fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentage (%)')
        ax.set_xlabel('Gender')
        plt.xticks(rotation=0)
        plt.legend(title='Churn')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/06_gender_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Gender analysis saved")
        
    def senior_citizen_analysis(self):
        """Senior citizen analysis"""
        fig, ax = plt.subplots(figsize=(8, 5))
        senior_churn = pd.crosstab(self.df['Senior Citizen'], self.df['Churn Label'], normalize='index') * 100
        senior_churn.plot(kind='bar', color=['#2ecc71', '#e74c3c'], ax=ax)
        ax.set_title('Churn Rate: Senior Citizen vs Non-Senior', fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentage (%)')
        ax.set_xlabel('Senior Citizen Status')
        plt.xticks(rotation=0)
        plt.legend(title='Churn')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/07_senior_citizen_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Senior citizen analysis saved")
        
    def payment_method_analysis(self):
        """Payment method analysis"""
        fig, ax = plt.subplots(figsize=(12, 5))
        payment_churn = pd.crosstab(self.df['Payment Method'], self.df['Churn Label'], normalize='index') * 100
        payment_churn.plot(kind='bar', color=['#2ecc71', '#e74c3c'], ax=ax)
        ax.set_title('Churn Rate by Payment Method', fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentage (%)')
        ax.set_xlabel('Payment Method')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Churn')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/08_payment_method_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Payment method analysis saved")
        
    def correlation_heatmap(self):
        """Correlation heatmap"""
        fig, ax = plt.subplots(figsize=(12, 8))
        numeric_df = self.df.select_dtypes(include=[np.number])
        correlation = numeric_df.corr()
        sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', ax=ax, cbar_kws={'label': 'Correlation'})
        ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/09_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Correlation heatmap saved")
        
    def generate_summary_stats(self):
        """Generate summary statistics"""
        print("\n" + "="*60)
        print("📊 EXPLORATORY DATA ANALYSIS SUMMARY")
        print("="*60)
        print(f"\n🔢 Total Customers: {len(self.df):,}")
        print(f"📉 Churned Customers: {self.df['Churn Value'].sum():,} ({self.df['Churn Value'].mean()*100:.2f}%)")
        print(f"📈 Retained Customers: {len(self.df) - self.df['Churn Value'].sum():,} ({(1-self.df['Churn Value'].mean())*100:.2f}%)")
        print(f"\n💰 Average Monthly Charges: ${self.df['Monthly Charges'].mean():.2f}")
        print(f"💰 Average Total Charges: ${pd.to_numeric(self.df['Total Charges'], errors='coerce').mean():.2f}")
        print(f"⏱️ Average Tenure: {self.df['Tenure Months'].mean():.1f} months")
        print(f"\n🔗 Contract Types:")
        print(self.df['Contract'].value_counts())
        print(f"\n📡 Internet Service Types:")
        print(self.df['Internet Service'].value_counts())
        print("="*60)
        
    def run_all(self):
        """Run all analyses"""
        print("🚀 Starting Exploratory Data Analysis...\n")
        self.churn_distribution()
        self.tenure_vs_churn()
        self.monthly_charges_vs_churn()
        self.contract_type_analysis()
        self.internet_service_analysis()
        self.gender_analysis()
        self.senior_citizen_analysis()
        self.payment_method_analysis()
        self.correlation_heatmap()
        self.generate_summary_stats()
        print("\n✅ All analyses completed! Check 'Images' folder for visualizations.")

# Main execution
if __name__ == "__main__":
    eda = ExploratoryAnalysis("data/cleaned_data.csv")
    eda.run_all()