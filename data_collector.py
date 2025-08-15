import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time

class VahanDataCollector:
    """
    Data collector for Vahan Dashboard vehicle registration data
    """
    
    def __init__(self):
        self.base_url = "https://vahan.parivahan.gov.in"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_vehicle_data(self, start_date=None, end_date=None):
        """
        Collect vehicle registration data from Vahan Dashboard
        For demo purposes, we'll create sample data that matches the expected structure
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=365*3)  # 3 years back
        if not end_date:
            end_date = datetime.now()
        
        # Generate sample data for demonstration
        data = self._generate_sample_data(start_date, end_date)
        return data
    
    def _generate_sample_data(self, start_date, end_date):
        """
        Generate sample vehicle registration data for dashboard demo
        """
        import numpy as np
        
        # Vehicle categories
        categories = ['2W', '3W', '4W']
        
        # Major manufacturers
        manufacturers = {
            '2W': ['Hero MotoCorp', 'Honda', 'TVS', 'Bajaj', 'Yamaha'],
            '3W': ['Bajaj', 'Mahindra', 'TVS', 'Piaggio', 'Atul Auto'],
            '4W': ['Maruti Suzuki', 'Hyundai', 'Tata', 'Mahindra', 'Kia']
        }
        
        # Generate monthly data
        data_points = []
        current_date = start_date
        
        while current_date <= end_date:
            for category in categories:
                for manufacturer in manufacturers[category]:
                    # Base registrations with some randomness
                    base_registrations = {
                        '2W': np.random.randint(8000, 15000),
                        '3W': np.random.randint(1000, 3000),
                        '4W': np.random.randint(5000, 12000)
                    }
                    
                    # Add seasonal and growth trends
                    month_factor = 1 + 0.1 * np.sin(2 * np.pi * current_date.month / 12)
                    year_growth = 1 + 0.05 * (current_date.year - start_date.year)
                    
                    registrations = int(base_registrations[category] * month_factor * year_growth)
                    
                    data_points.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'year': current_date.year,
                        'quarter': f"Q{((current_date.month-1)//3)+1}",
                        'month': current_date.month,
                        'vehicle_category': category,
                        'manufacturer': manufacturer,
                        'registrations': registrations
                    })
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        return pd.DataFrame(data_points)
    
    def save_data(self, data, filename='vehicle_data.csv'):
        """Save data to CSV file"""
        filepath = f"C:\\Users\\91766\\Downloads\\vahan-insights\\{filename}"
        data.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
        return filepath

if __name__ == "__main__":
    collector = VahanDataCollector()
    data = collector.get_vehicle_data()
    collector.save_data(data)
    print(f"Collected {len(data)} data points")