import pandas as pd
import random
from datetime import datetime, timedelta

def generate_mock_data(filename='target_20260214.xlsx', num_rows=50):
    prefixes = ['1', '2', '3', '4', '5']
    groups = ['1교구', '1교구/무소속', '2교구', '2교구/무소속', '3교구', '3교구/무소속', '4교구', 'Other']
    
    data = []
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2010, 12, 31)
    
    for i in range(num_rows):
        days_between_dates = (end_date - start_date).days
        random_number_of_days = random.randrange(days_between_dates)
        bod = start_date + timedelta(days=random_number_of_days)
        group = random.choice(groups)
        
        row = {
            'Name': f'Person_{i}',
            'BOD': bod,
            'Group': group,
            'type': 'TypeA',
            'status': 'Active',
            'registerdate': datetime.now(),
            'type.1': 'TypeB',
            'address': f'Address_{random.randint(1, 10)}'
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    
    print(f"Saving mock data to {filename}...")
    try:
        df.to_excel(filename, index=False) # Default engine openpyxl
        print("Success.")
    except Exception as e:
        print(f"Error saving mock data: {e}")

if __name__ == "__main__":
    generate_mock_data()
