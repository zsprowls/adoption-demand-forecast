#!/usr/bin/env python3
"""
Test script for the Adoption Demand Forecast Tool

This script tests the main functionality of the forecast tool.
"""

import os
import sys
from forecast import AdoptionForecast

def test_forecast_tool():
    """Test the forecast tool with sample data."""
    
    print("🧪 Testing Adoption Demand Forecast Tool")
    print("=" * 50)
    
    # Check if sample data exists
    sample_file = "sample_adoption_data.csv"
    if not os.path.exists(sample_file):
        print("❌ Sample data not found. Please run 'python generate_sample_data.py' first.")
        return False
    
    try:
        # Initialize forecast tool
        print("📊 Loading sample data...")
        forecast = AdoptionForecast(sample_file)
        
        # Test basic calculations
        print("🧮 Testing counselor needs calculation...")
        results = forecast.calculate_counselor_needs(
            avg_time_per_adoption=30,
            non_adopting_percentage=30,
            num_counselors=3
        )
        
        # Verify results
        assert results['avg_daily_adoptions'] > 0, "Average daily adoptions should be positive"
        assert results['total_counselor_hours'] > 0, "Total counselor hours should be positive"
        assert results['hours_per_counselor'] > 0, "Hours per counselor should be positive"
        
        print("✅ Basic calculations passed!")
        
        # Test data loading
        assert len(forecast.data) > 0, "Data should not be empty"
        assert 'DateTime' in forecast.data.columns, "DateTime column should exist"
        assert 'Species' in forecast.data.columns, "Species column should exist"
        
        print("✅ Data loading passed!")
        
        # Test data processing
        assert 'Hour' in forecast.processed_data.columns, "Hour column should be created"
        assert 'DayOfWeek' in forecast.processed_data.columns, "DayOfWeek column should be created"
        
        print("✅ Data processing passed!")
        
        # Print summary
        print("\n📋 Test Results Summary:")
        print(f"   • Total records: {len(forecast.data)}")
        print(f"   • Date range: {forecast.data['DateTime'].min().strftime('%Y-%m-%d')} to {forecast.data['DateTime'].max().strftime('%Y-%m-%d')}")
        print(f"   • Species: {', '.join(forecast.data['Species'].unique())}")
        print(f"   • Average daily adoptions: {results['avg_daily_adoptions']:.1f}")
        print(f"   • Total counselor hours needed: {results['total_counselor_hours']:.1f}")
        print(f"   • Hours per counselor: {results['hours_per_counselor']:.1f}")
        
        print("\n🎉 All tests passed! The tool is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_visualizations():
    """Test that visualizations can be created without errors."""
    
    print("\n🎨 Testing visualization generation...")
    
    try:
        sample_file = "sample_adoption_data.csv"
        if not os.path.exists(sample_file):
            print("❌ Sample data not found. Skipping visualization tests.")
            return False
        
        forecast = AdoptionForecast(sample_file)
        
        # Test that visualization methods don't crash
        print("   • Testing daily trends plot...")
        daily_data = forecast.plot_adoptions_per_day()
        
        print("   • Testing hourly analysis plot...")
        hourly_data = forecast.plot_adoptions_per_hour()
        
        print("   • Testing distribution plot...")
        forecast.plot_adoption_distribution()
        
        print("   • Testing counselor capacity summary...")
        results = forecast.calculate_counselor_needs(30, 30, 3)
        forecast.plot_counselor_capacity_summary(results)
        
        print("✅ All visualizations generated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

if __name__ == "__main__":
    print("🐾 Adoption Demand Forecast Tool - Test Suite")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_forecast_tool()
    test2_passed = test_visualizations()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ The adoption demand forecast tool is working correctly.")
        print("📋 You can now:")
        print("   • Run 'python forecast.py' for command-line interface")
        print("   • Run 'streamlit run streamlit_app.py' for web interface")
        print("   • Use your own CSV data files")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\n🔧 Troubleshooting:")
        print("   • Make sure you've run 'python generate_sample_data.py'")
        print("   • Check that all dependencies are installed: 'pip install -r requirements.txt'")
        print("   • Verify Python version is 3.7+")
    
    print("\n" + "=" * 60) 