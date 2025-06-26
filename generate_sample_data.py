#!/usr/bin/env python3
"""
Sample Data Generator for Adoption Demand Forecast Tool

This script generates realistic sample adoption data for testing the forecast tool.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_records=1000, output_file='sample_adoption_data.csv'):
    """
    Generate sample adoption data with realistic patterns.
    
    Args:
        num_records (int): Number of adoption records to generate
        output_file (str): Output CSV file name
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define date range (last 6 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    # Generate random dates
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    dates = np.random.choice(date_range, num_records)
    
    # Generate times with realistic patterns (more adoptions during business hours)
    # Peak hours: 10-16 (10 AM to 4 PM)
    # Moderate hours: 9, 17-19 (9 AM, 5-7 PM)
    # Low hours: 8, 20-21 (8 AM, 8-9 PM)
    
    hour_weights = {
        8: 0.05,   # 8 AM - low
        9: 0.12,   # 9 AM - moderate
        10: 0.15,  # 10 AM - peak
        11: 0.15,  # 11 AM - peak
        12: 0.12,  # 12 PM - moderate
        13: 0.08,  # 1 PM - moderate
        14: 0.12,  # 2 PM - moderate
        15: 0.15,  # 3 PM - peak
        16: 0.15,  # 4 PM - peak
        17: 0.12,  # 5 PM - moderate
        18: 0.08,  # 6 PM - moderate
        19: 0.03,  # 7 PM - low
        20: 0.01,  # 8 PM - very low
        21: 0.01   # 9 PM - very low
    }
    
    # Normalize weights to sum to 1
    total_weight = sum(hour_weights.values())
    normalized_weights = {hour: weight/total_weight for hour, weight in hour_weights.items()}
    
    hours = np.random.choice(list(normalized_weights.keys()), num_records, p=list(normalized_weights.values()))
    minutes = np.random.randint(0, 60, num_records)
    
    # Combine dates and times
    datetimes = []
    for date, hour, minute in zip(dates, hours, minutes):
        # Convert numpy.datetime64 to pandas.Timestamp for .replace()
        if not isinstance(date, pd.Timestamp):
            date = pd.Timestamp(date)
        dt = date.replace(hour=hour, minute=minute)
        datetimes.append(dt)
    
    # Generate animal numbers
    animal_numbers = [f"A{str(i).zfill(4)}" for i in range(1, num_records + 1)]
    
    # Generate species with realistic distribution
    species_weights = {'Dog': 0.60, 'Cat': 0.35, 'Other': 0.05}
    species = np.random.choice(list(species_weights.keys()), num_records, p=list(species_weights.values()))
    
    # All outcomes are "Adoption"
    outcomes = ['Adoption'] * num_records
    
    # Create DataFrame
    data = pd.DataFrame({
        'Outcome': outcomes,
        'AnimalNumber': animal_numbers,
        'Species': species,
        'DateTime': datetimes
    })
    
    # Sort by datetime
    data = data.sort_values('DateTime').reset_index(drop=True)
    
    # Save to CSV
    data.to_csv(output_file, index=False)
    
    print(f"✅ Generated {num_records} sample adoption records")
    print(f"📁 Saved to: {output_file}")
    print(f"📅 Date range: {data['DateTime'].min().strftime('%Y-%m-%d')} to {data['DateTime'].max().strftime('%Y-%m-%d')}")
    print(f"🐕 Species breakdown:")
    print(data['Species'].value_counts())
    
    return data

def generate_weekend_heavy_data(num_records=1000, output_file='sample_weekend_data.csv'):
    """
    Generate sample data with heavier weekend adoption patterns.
    
    Args:
        num_records (int): Number of adoption records to generate
        output_file (str): Output CSV file name
    """
    
    np.random.seed(42)
    random.seed(42)
    
    # Define date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    # Generate dates with weekend bias
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Weekend days (Saturday=5, Sunday=6) get higher weights
    weekend_dates = [d for d in date_range if d.weekday() >= 5]
    weekday_dates = [d for d in date_range if d.weekday() < 5]
    
    # 70% weekend, 30% weekday
    weekend_count = int(num_records * 0.7)
    weekday_count = num_records - weekend_count
    
    weekend_selection = np.random.choice(weekend_dates, weekend_count)
    weekday_selection = np.random.choice(weekday_dates, weekday_count)
    
    dates = np.concatenate([weekend_selection, weekday_selection])
    
    # Generate times (similar to above but with more variation)
    hour_weights = {
        8: 0.03,   # 8 AM
        9: 0.10,   # 9 AM
        10: 0.15,  # 10 AM
        11: 0.15,  # 11 AM
        12: 0.10,  # 12 PM
        13: 0.08,  # 1 PM
        14: 0.10,  # 2 PM
        15: 0.15,  # 3 PM
        16: 0.15,  # 4 PM
        17: 0.10,  # 5 PM
        18: 0.06,  # 6 PM
        19: 0.02,  # 7 PM
        20: 0.01,  # 8 PM
        21: 0.01   # 9 PM
    }
    
    # Normalize weights to sum to 1
    total_weight = sum(hour_weights.values())
    normalized_weights = {hour: weight/total_weight for hour, weight in hour_weights.items()}
    
    hours = np.random.choice(list(normalized_weights.keys()), num_records, p=list(normalized_weights.values()))
    minutes = np.random.randint(0, 60, num_records)
    
    # Combine dates and times
    datetimes = []
    for date, hour, minute in zip(dates, hours, minutes):
        if not isinstance(date, pd.Timestamp):
            date = pd.Timestamp(date)
        dt = date.replace(hour=hour, minute=minute)
        datetimes.append(dt)
    
    # Generate animal numbers
    animal_numbers = [f"A{str(i).zfill(4)}" for i in range(1, num_records + 1)]
    
    # Generate species
    species_weights = {'Dog': 0.65, 'Cat': 0.30, 'Other': 0.05}
    species = np.random.choice(list(species_weights.keys()), num_records, p=list(species_weights.values()))
    
    # All outcomes are "Adoption"
    outcomes = ['Adoption'] * num_records
    
    # Create DataFrame
    data = pd.DataFrame({
        'Outcome': outcomes,
        'AnimalNumber': animal_numbers,
        'Species': species,
        'DateTime': datetimes
    })
    
    # Sort by datetime
    data = data.sort_values('DateTime').reset_index(drop=True)
    
    # Save to CSV
    data.to_csv(output_file, index=False)
    
    print(f"✅ Generated {num_records} weekend-heavy adoption records")
    print(f"📁 Saved to: {output_file}")
    print(f"📅 Date range: {data['DateTime'].min().strftime('%Y-%m-%d')} to {data['DateTime'].max().strftime('%Y-%m-%d')}")
    
    # Show day of week distribution
    data['DayOfWeek'] = data['DateTime'].dt.day_name()
    print(f"📊 Day of week distribution:")
    print(data['DayOfWeek'].value_counts().sort_index())
    
    return data

if __name__ == "__main__":
    print("🐾 Sample Data Generator for Adoption Demand Forecast")
    print("=" * 50)
    
    # Generate standard sample data
    print("\n1. Generating standard sample data...")
    generate_sample_data(1000, 'sample_adoption_data.csv')
    
    # Generate weekend-heavy data
    print("\n2. Generating weekend-heavy sample data...")
    generate_weekend_heavy_data(1000, 'sample_weekend_data.csv')
    
    print("\n✅ Sample data generation complete!")
    print("\n📋 You can now use these files to test the forecast tool:")
    print("   • python3 forecast.py (then enter 'sample_adoption_data.csv')")
    print("   • streamlit run streamlit_app.py (then upload either CSV file)") 