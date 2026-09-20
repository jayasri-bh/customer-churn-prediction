import os
import pandas as pd
import numpy as np
from datetime import datetime
class ReportGenerator:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        os.makedirs("reports", exist_ok=True)  # ADD THIS LINE
        self.report_file = "reports/Churn_Analysis_Report.txt"
        
    def generate_report(self):
        """Generate comprehensive churn analysis report"""
        
        report = []
        report.append("="*80)
        report.append("CUSTOMER CHURN ANALYSIS REPORT")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Executive Summary
        report.append("\n" + "="*80)
        report.append("1. EXECUTIVE SUMMARY")
        report.append("="*80)
        
        total_customers = len(self.df)
        churned = self.df['Churn Value'].sum()
        churn_rate = (churned / total_customers) * 100
        retained = total_customers - churned
        
        report.append(f"Total Customers:        {total_customers:,}")
        report.append(f"Churned Customers:      {churned:,}")
        report.append(f"Retained Customers:     {retained:,}")
        report.append(f"Churn Rate:             {churn_rate:.2f}%")
        report.append(f"Retention Rate:         {100-churn_rate:.2f}%\n")
        
        # Financial Metrics
        report.append("\n" + "="*80)
        report.append("2. FINANCIAL METRICS")
        report.append("="*80)
        
        avg_monthly = self.df['Monthly Charges'].mean()
        total_charges = pd.to_numeric(self.df['Total Charges'], errors='coerce').sum()
        churned_revenue = self.df[self.df['Churn Value'] == 1]['Monthly Charges'].sum()
        retained_revenue = self.df[self.df['Churn Value'] == 0]['Monthly Charges'].sum()
        
        report.append(f"Average Monthly Charges:     ${avg_monthly:.2f}")
        report.append(f"Total Annual Charges:        ${total_charges:,.2f}")
        report.append(f"Monthly Revenue (Churned):   ${churned_revenue:,.2f}")
        report.append(f"Monthly Revenue (Retained):  ${retained_revenue:,.2f}\n")
        
        # Customer Demographics
        report.append("\n" + "="*80)
        report.append("3. CUSTOMER DEMOGRAPHICS")
        report.append("="*80)
        
        report.append(f"\nGender Distribution:")
        for gender, count in self.df['Gender'].value_counts().items():
            pct = (count / total_customers) * 100
            report.append(f"  {gender}: {count:,} ({pct:.1f}%)")
            
        report.append(f"\nSenior Citizen Status:")
        for status, count in self.df['Senior Citizen'].value_counts().items():
            pct = (count / total_customers) * 100
            report.append(f"  {status}: {count:,} ({pct:.1f}%)")
            
        report.append(f"\nFamily Status:")
        for status in ['Partner', 'Dependents']:
            for val, count in self.df[status].value_counts().items():
                pct = (count / total_customers) * 100
                report.append(f"  {status} - {val}: {count:,} ({pct:.1f}%)")
        
        # Tenure Analysis
        report.append("\n\n" + "="*80)
        report.append("4. TENURE ANALYSIS")
        report.append("="*80)
        
        avg_tenure = self.df['Tenure Months'].mean()
        churn_by_tenure = self.df.groupby(pd.cut(self.df['Tenure Months'], bins=[0, 6, 12, 24, 72]))['Churn Value'].agg(['sum', 'count'])
        
        report.append(f"Average Tenure: {avg_tenure:.1f} months\n")
        report.append("Churn Rate by Tenure:")
        tenure_labels = ['0-6 months', '6-12 months', '12-24 months', '24+ months']
        for i, (label) in enumerate(tenure_labels):
            if i < len(churn_by_tenure):
                churn_count = churn_by_tenure.iloc[i]['sum']
                total_count = churn_by_tenure.iloc[i]['count']
                churn_pct = (churn_count / total_count) * 100
                report.append(f"  {label}: {churn_pct:.1f}% ({int(churn_count)}/{int(total_count)})")
        
        # Service Analysis
        report.append("\n\n" + "="*80)
        report.append("5. SERVICE ANALYSIS")
        report.append("="*80)
        
        report.append("\nInternet Service Type:")
        internet_churn = pd.crosstab(self.df['Internet Service'], self.df['Churn Label'])
        for service in self.df['Internet Service'].unique():
            churn_count = internet_churn.loc[service, 'Yes'] if 'Yes' in internet_churn.columns else 0
            total_count = internet_churn.loc[service].sum()
            pct = (churn_count / total_count) * 100
            report.append(f"  {service}: {pct:.1f}% churn rate ({int(churn_count)}/{int(total_count)})")
            
        report.append("\nContract Type:")
        contract_churn = pd.crosstab(self.df['Contract'], self.df['Churn Label'])
        for contract in self.df['Contract'].unique():
            churn_count = contract_churn.loc[contract, 'Yes'] if 'Yes' in contract_churn.columns else 0
            total_count = contract_churn.loc[contract].sum()
            pct = (churn_count / total_count) * 100
            report.append(f"  {contract}: {pct:.1f}% churn rate ({int(churn_count)}/{int(total_count)})")
        
        # Top Churn Reasons
        report.append("\n\n" + "="*80)
        report.append("6. TOP CHURN REASONS")
        report.append("="*80)
        
        churn_reasons = self.df[self.df['Churn Value'] == 1]['Churn Reason'].value_counts().head(10)
        report.append("\nTop 10 Reasons for Churn:")
        for i, (reason, count) in enumerate(churn_reasons.items(), 1):
            pct = (count / churned) * 100
            report.append(f"  {i}. {reason}: {count} ({pct:.1f}%)")
        
        # Key Insights
        report.append("\n\n" + "="*80)
        report.append("7. KEY INSIGHTS & RECOMMENDATIONS")
        report.append("="*80)
        
        report.append("\n✓ KEY FINDINGS:")
        
        # Insight 1: Tenure
        if avg_tenure < 24:
            report.append(f"  • Average customer tenure is only {avg_tenure:.1f} months")
            report.append("    → Focus on improving early retention (first 6 months)")
        
        # Insight 2: Contract
        month_to_month = self.df[self.df['Contract'] == 'Month-to-month']['Churn Value'].mean() * 100
        if month_to_month > 40:
            report.append(f"  • Month-to-month contracts have {month_to_month:.1f}% churn rate")
            report.append("    → Incentivize customers to switch to longer contracts")
        
        # Insight 3: Internet Service
        fiber_churn = self.df[self.df['Internet Service'] == 'Fiber optic']['Churn Value'].mean() * 100
        if fiber_churn > 40:
            report.append(f"  • Fiber optic customers have {fiber_churn:.1f}% churn rate")
            report.append("    → Address service quality issues with Fiber optic users")
        
        # Insight 4: Monthly Charges
        avg_churned_charges = self.df[self.df['Churn Value'] == 1]['Monthly Charges'].mean()
        avg_retained_charges = self.df[self.df['Churn Value'] == 0]['Monthly Charges'].mean()
        if avg_churned_charges > avg_retained_charges:
            report.append(f"  • Churned customers pay ${avg_churned_charges:.2f}/month (vs ${avg_retained_charges:.2f} for retained)")
            report.append("    → Consider pricing review for high-value customers")
        
        report.append("\n✓ RECOMMENDATIONS:")
        report.append("  1. Implement targeted retention programs for month-to-month customers")
        report.append("  2. Improve Fiber optic service quality and customer support")
        report.append("  3. Create early engagement programs for new customers (first 6 months)")
        report.append("  4. Review pricing strategy to reduce cost-driven churn")
        report.append("  5. Address top churn reasons with specific action plans")
        
        report.append("\n" + "="*80)
        report.append("END OF REPORT")
        report.append("="*80)
        
        # Save report
        report_text = "\n".join(report)
        with open(self.report_file, 'w', encoding='utf-8') as f:
          f.write(report_text)
            
        print(report_text)
        print(f"\n✅ Report saved to: {self.report_file}")

# Main execution
if __name__ == "__main__":
    generator = ReportGenerator("data/cleaned_data.csv")
    generator.generate_report()