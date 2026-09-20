import pandas as pd
import numpy as np

class PowerBIDataPrep:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        
    def prepare_dashboard_data(self):
        """Prepare data for Power BI"""
        
        # Create summary by various dimensions
        summaries = {}
        
        # 1. Overall Metrics
        print("📊 Creating dashboard data...\n")
        
        overall = pd.DataFrame({
            'Metric': ['Total Customers', 'Churned', 'Retained', 'Churn Rate %', 'Avg Monthly Charges', 'Avg Tenure Months'],
            'Value': [
                len(self.df),
                self.df['Churn Value'].sum(),
                len(self.df) - self.df['Churn Value'].sum(),
                round(self.df['Churn Value'].mean() * 100, 2),
                round(self.df['Monthly Charges'].mean(), 2),
                round(self.df['Tenure Months'].mean(), 2)
            ]
        })
        overall.to_csv('data/dashboard_overall_metrics.csv', index=False)
        print("✅ Overall metrics saved")
        
        # 2. Churn by Internet Service
        internet_service = pd.crosstab(
            self.df['Internet Service'], 
            self.df['Churn Label'], 
            margins=True
        )
        internet_service.to_csv('data/dashboard_internet_service.csv')
        print("✅ Internet service analysis saved")
        
        # 3. Churn by Contract
        contract = pd.crosstab(
            self.df['Contract'], 
            self.df['Churn Label'], 
            margins=True
        )
        contract.to_csv('data/dashboard_contract.csv')
        print("✅ Contract analysis saved")
        
        # 4. Churn by Tenure Bins
        self.df['Tenure_Bin'] = pd.cut(self.df['Tenure Months'], 
                                        bins=[0, 6, 12, 24, 72],
                                        labels=['0-6 months', '6-12 months', '12-24 months', '24+ months'])
        tenure_churn = pd.crosstab(
            self.df['Tenure_Bin'], 
            self.df['Churn Label'], 
            margins=True
        )
        tenure_churn.to_csv('data/dashboard_tenure.csv')
        print("✅ Tenure analysis saved")
        
        # 5. Churn by Gender
        gender = pd.crosstab(
            self.df['Gender'], 
            self.df['Churn Label'], 
            margins=True
        )
        gender.to_csv('data/dashboard_gender.csv')
        print("✅ Gender analysis saved")
        
        # 6. Churn by Senior Citizen
        senior = pd.crosstab(
            self.df['Senior Citizen'], 
            self.df['Churn Label'], 
            margins=True
        )
        senior.to_csv('data/dashboard_senior_citizen.csv')
        print("✅ Senior citizen analysis saved")
        
        # 7. Churn by Payment Method
        payment = pd.crosstab(
            self.df['Payment Method'], 
            self.df['Churn Label'], 
            margins=True
        )
        payment.to_csv('data/dashboard_payment_method.csv')
        print("✅ Payment method analysis saved")
        
        # 8. Monthly Charges Analysis
        charges_churn = self.df.groupby('Churn Label').agg({
            'Monthly Charges': ['count', 'mean', 'min', 'max', 'median']
        }).round(2)
        charges_churn.to_csv('data/dashboard_charges.csv')
        print("✅ Charges analysis saved")
        
        # 9. Services Subscribed (count by churn)
        services = ['Online Security', 'Online Backup', 'Device Protection', 'Tech Support', 'Streaming TV', 'Streaming Movies']
        service_data = []
        
        for service in services:
            for churn_status in ['Yes', 'No']:
                count = len(self.df[(self.df[service] == 'Yes') & (self.df['Churn Label'] == churn_status)])
                service_data.append({
                    'Service': service,
                    'Churn_Status': churn_status,
                    'Count': count
                })
        
        services_df = pd.DataFrame(service_data)
        services_df.to_csv('data/dashboard_services.csv', index=False)
        print("✅ Services analysis saved")
        
        # 10. Geographic Data (State)
        state_churn = pd.crosstab(
            self.df['State'], 
            self.df['Churn Label']
        ).reset_index()

# Handle different column names
        if 'Yes' in state_churn.columns and 'No' in state_churn.columns:
            state_churn['Total'] = state_churn['No'] + state_churn['Yes']
            state_churn['Churn_Rate_%'] = round((state_churn['Yes'] / state_churn['Total']) * 100, 2)
        else:
    # If columns are 0 and 1 instead of No and Yes
             state_churn['Total'] = state_churn.iloc[:, 1] + state_churn.iloc[:, 2]
             state_churn['Churn_Rate_%'] = round((state_churn.iloc[:, 2] / state_churn['Total']) * 100, 2)

        state_churn = state_churn.sort_values('Churn_Rate_%', ascending=False).head(20)
        state_churn.to_csv('data/dashboard_state.csv', index=False)
        print("✅ State analysis saved")
        
        print("\n" + "="*60)
        print("✅ All Power BI data files created in 'data' folder!")
        print("="*60)
        print("\nFiles created:")
        print("  1. dashboard_overall_metrics.csv")
        print("  2. dashboard_internet_service.csv")
        print("  3. dashboard_contract.csv")
        print("  4. dashboard_tenure.csv")
        print("  5. dashboard_gender.csv")
        print("  6. dashboard_senior_citizen.csv")
        print("  7. dashboard_payment_method.csv")
        print("  8. dashboard_charges.csv")
        print("  9. dashboard_services.csv")
        print("  10. dashboard_state.csv")
        print("\n🎯 Next: Import these CSVs into Power BI")

# Main execution
if __name__ == "__main__":
    prep = PowerBIDataPrep("data/cleaned_data.csv")
    prep.prepare_dashboard_data()