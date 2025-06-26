#!/usr/bin/env python3
"""
Adoption Demand Forecast Tool

A Python tool for analyzing animal adoption data and forecasting counselor time needs.
"""

import pandas as pd
import matplotlib
# Set matplotlib to use non-interactive backend to prevent pop-up windows
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AdoptionForecast:
    """Main class for adoption demand forecasting."""
    
    def __init__(self, csv_file_path):
        """
        Initialize the forecast tool with adoption data.
        
        Args:
            csv_file_path (str): Path to the CSV file containing adoption data
        """
        self.csv_file_path = csv_file_path
        self.data = None
        self.processed_data = None
        self.load_data()
        
    def load_data(self):
        """Load and preprocess the adoption data."""
        try:
            # Load CSV file
            self.data = pd.read_csv(self.csv_file_path)
            
            # Convert DateTime column to datetime
            self.data['DateTime'] = pd.to_datetime(self.data['DateTime'])
            
            # Extract additional time features
            self.data['Date'] = self.data['DateTime'].dt.date
            self.data['Hour'] = self.data['DateTime'].dt.hour
            self.data['DayOfWeek'] = self.data['DateTime'].dt.day_name()
            self.data['Month'] = self.data['DateTime'].dt.month
            self.data['Year'] = self.data['DateTime'].dt.year
            
            # Create processed data for analysis
            self.processed_data = self.data.copy()
            
            print(f"Successfully loaded {len(self.data)} adoption records")
            print(f"Date range: {self.data['DateTime'].min()} to {self.data['DateTime'].max()}")
            print(f"Species: {self.data['Species'].unique()}")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def plot_adoptions_per_day(self, show_plot=True):
        """Create a plot showing adoptions per day."""
        daily_adoptions = self.data.groupby('Date').size().reset_index(name='Adoptions')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_adoptions['Date'], daily_adoptions['Adoptions'], marker='o', linewidth=2, markersize=4)
        ax.set_title('Adoptions per Day', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Number of Adoptions', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
        
        # Add trend line
        z = np.polyfit(range(len(daily_adoptions)), daily_adoptions['Adoptions'], 1)
        p = np.poly1d(z)
        ax.plot(daily_adoptions['Date'], p(range(len(daily_adoptions))), "r--", alpha=0.8, label='Trend')
        ax.legend()
        
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return daily_adoptions
    
    def plot_adoptions_per_hour(self, plot_type='density', show_plot=True):
        """
        Create a plot showing adoptions per hour of day.
        
        Args:
            plot_type (str): 'density' for bell curve, 'bar' for bar chart
            show_plot (bool): Whether to display the plot
        """
        hourly_adoptions = self.data.groupby('Hour').size().reset_index(name='Adoptions')
        
        if plot_type == 'density':
            # Create density plot (bell curve)
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Fit a normal distribution
            mean_hour = hourly_adoptions['Hour'].mean()
            std_hour = hourly_adoptions['Hour'].std()
            
            # Create smooth curve
            x_smooth = np.linspace(0, 23, 100)
            y_smooth = stats.norm.pdf(x_smooth, mean_hour, std_hour) * len(self.data) / 24
            
            ax.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='Fitted Normal Distribution')
            ax.bar(hourly_adoptions['Hour'], hourly_adoptions['Adoptions'], alpha=0.6, color='skyblue', label='Actual Data')
            
            ax.set_title('Adoptions per Hour of Day (Density Plot)', fontsize=16, fontweight='bold')
            ax.set_xlabel('Hour of Day', fontsize=12)
            ax.set_ylabel('Number of Adoptions', fontsize=12)
            ax.set_xticks(range(0, 24, 2))
            ax.grid(True, alpha=0.3)
            ax.legend()
            
        else:
            # Create bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(hourly_adoptions['Hour'], hourly_adoptions['Adoptions'], color='skyblue', alpha=0.7)
            ax.set_title('Adoptions per Hour of Day', fontsize=16, fontweight='bold')
            ax.set_xlabel('Hour of Day', fontsize=12)
            ax.set_ylabel('Number of Adoptions', fontsize=12)
            ax.set_xticks(range(0, 24, 2))
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return hourly_adoptions
    
    def plot_adoption_distribution(self, filter_day=None, filter_species=None, show_plot=True):
        """
        Create distribution plots with optional filtering.
        
        Args:
            filter_day (str): Day of week to filter by (e.g., 'Monday')
            filter_species (str): Species to filter by (e.g., 'Dog')
            show_plot (bool): Whether to display the plot
        """
        filtered_data = self.data.copy()
        
        if filter_day:
            filtered_data = filtered_data[filtered_data['DayOfWeek'] == filter_day]
            title_suffix = f" - {filter_day}s"
        else:
            title_suffix = ""
            
        if filter_species:
            filtered_data = filtered_data[filtered_data['Species'] == filter_species]
            title_suffix += f" - {filter_species}s"
        
        if len(filtered_data) == 0:
            print("No data matches the specified filters.")
            return
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Hourly distribution
        hourly_dist = filtered_data.groupby('Hour').size()
        ax1.bar(hourly_dist.index, hourly_dist.values, color='lightcoral', alpha=0.7)
        ax1.set_title(f'Hourly Distribution{title_suffix}', fontweight='bold')
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Adoptions')
        ax1.set_xticks(range(0, 24, 2))
        ax1.grid(True, alpha=0.3)
        
        # 2. Day of week distribution
        day_dist = filtered_data.groupby('DayOfWeek').size()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_dist = day_dist.reindex(day_order, fill_value=0)
        ax2.bar(range(len(day_dist)), day_dist.values, color='lightgreen', alpha=0.7)
        ax2.set_title(f'Day of Week Distribution{title_suffix}', fontweight='bold')
        ax2.set_xlabel('Day of Week')
        ax2.set_ylabel('Adoptions')
        ax2.set_xticks(range(len(day_dist)))
        ax2.set_xticklabels(day_dist.index, rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # 3. Species distribution
        species_dist = filtered_data.groupby('Species').size()
        ax3.pie(species_dist.values, labels=species_dist.index, autopct='%1.1f%%', startangle=90)
        ax3.set_title(f'Species Distribution{title_suffix}', fontweight='bold')
        
        # 4. Monthly trend
        monthly_dist = filtered_data.groupby(['Year', 'Month']).size().reset_index(name='Adoptions')
        monthly_dist['Date'] = pd.to_datetime(monthly_dist[['Year', 'Month']].assign(day=1))
        ax4.plot(monthly_dist['Date'], monthly_dist['Adoptions'], marker='o', linewidth=2)
        ax4.set_title(f'Monthly Trend{title_suffix}', fontweight='bold')
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Adoptions')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return filtered_data
    
    def calculate_counselor_needs(self, avg_time_per_adoption, non_adopting_percentage, num_counselors):
        """
        Calculate counselor time needs and workload distribution.
        
        Args:
            avg_time_per_adoption (int): Average time per adoption in minutes
            non_adopting_percentage (float): Percentage of non-adopting visitors (0-100)
            num_counselors (int): Number of counselors working
            
        Returns:
            dict: Dictionary containing calculated metrics
        """
        # Calculate total adoptions per day
        daily_adoptions = self.data.groupby('Date').size().reset_index(name='Adoptions')
        avg_daily_adoptions = daily_adoptions['Adoptions'].mean()
        
        # Calculate total time needed
        total_adoption_time = avg_daily_adoptions * avg_time_per_adoption  # minutes
        
        # Account for non-adopting visitors
        non_adopting_multiplier = 1 + (non_adopting_percentage / 100)
        total_counselor_time = total_adoption_time * non_adopting_multiplier
        
        # Convert to hours
        total_counselor_hours = total_counselor_time / 60
        
        # Calculate per-counselor workload
        hours_per_counselor = total_counselor_hours / num_counselors
        
        # Calculate peak hour analysis
        hourly_adoptions = self.data.groupby('Hour').size()
        peak_hour = hourly_adoptions.idxmax()
        peak_adoptions = hourly_adoptions.max()
        
        # Estimate peak hour workload
        peak_hour_time = peak_adoptions * avg_time_per_adoption * non_adopting_multiplier / 60  # hours
        peak_hour_per_counselor = peak_hour_time / num_counselors
        
        results = {
            'avg_daily_adoptions': avg_daily_adoptions,
            'total_adoption_time_minutes': total_adoption_time,
            'total_counselor_time_minutes': total_counselor_time,
            'total_counselor_hours': total_counselor_hours,
            'hours_per_counselor': hours_per_counselor,
            'peak_hour': peak_hour,
            'peak_adoptions': peak_adoptions,
            'peak_hour_time': peak_hour_time,
            'peak_hour_per_counselor': peak_hour_per_counselor,
            'num_counselors': num_counselors,
            'avg_time_per_adoption': avg_time_per_adoption,
            'non_adopting_percentage': non_adopting_percentage
        }
        
        return results
    
    def plot_counselor_capacity_summary(self, results, show_plot=True):
        """
        Create a comprehensive summary graph showing counselor capacity vs workload.
        
        Args:
            results (dict): Results from calculate_counselor_needs
            show_plot (bool): Whether to display the plot
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Daily Workload Distribution', 'Peak Hour Analysis', 
                          'Counselor Capacity vs Demand', 'Workload Breakdown'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "indicator"}, {"type": "pie"}]]
        )
        
        # 1. Daily workload distribution (simplified - showing average daily pattern)
        hourly_adoptions = self.data.groupby('Hour').size()
        hourly_workload = hourly_adoptions * results['avg_time_per_adoption'] * (1 + results['non_adopting_percentage']/100) / 60
        
        fig.add_trace(
            go.Bar(x=hourly_workload.index, y=hourly_workload.values, name='Workload (hours)'),
            row=1, col=1
        )
        
        # 2. Peak hour analysis
        fig.add_trace(
            go.Bar(x=[results['peak_hour']], y=[results['peak_hour_per_counselor']], 
                   name=f'Peak Hour ({results["peak_hour"]}:00)', marker_color='red'),
            row=1, col=2
        )
        
        # Add average line
        fig.add_hline(y=results['hours_per_counselor'], line_dash="dash", line_color="green",
                     annotation_text="Average Daily Workload", row=1, col=2)
        
        # 3. Capacity indicator
        capacity_utilization = (results['hours_per_counselor'] / 8) * 100  # Assuming 8-hour workday
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=capacity_utilization,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Daily Capacity Utilization (%)"},
                delta={'reference': 100},
                gauge={
                    'axis': {'range': [None, 120]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "orange"},
                        {'range': [100, 120], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 100
                    }
                }
            ),
            row=2, col=1
        )
        
        # 4. Workload breakdown pie chart
        adoption_time = results['total_adoption_time_minutes'] / 60
        non_adoption_time = (results['total_counselor_time_minutes'] - results['total_adoption_time_minutes']) / 60
        
        fig.add_trace(
            go.Pie(labels=['Adoption Time', 'Non-Adoption Time'], 
                   values=[adoption_time, non_adoption_time],
                   name="Time Breakdown"),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Counselor Capacity Analysis Summary",
            showlegend=False,
            height=800
        )
        
        if show_plot:
            fig.show()
        
        return fig
    
    def print_summary_report(self, results):
        """
        Print a comprehensive summary report.
        
        Args:
            results (dict): Results from calculate_counselor_needs
        """
        print("\n" + "="*60)
        print("ADOPTION DEMAND FORECAST SUMMARY REPORT")
        print("="*60)
        
        print(f"\n📊 DATA OVERVIEW:")
        print(f"   • Total adoption records: {len(self.data):,}")
        print(f"   • Date range: {self.data['DateTime'].min().strftime('%Y-%m-%d')} to {self.data['DateTime'].max().strftime('%Y-%m-%d')}")
        print(f"   • Average daily adoptions: {results['avg_daily_adoptions']:.1f}")
        print(f"   • Species: {', '.join(self.data['Species'].unique())}")
        
        print(f"\n⏰ TIME ANALYSIS:")
        print(f"   • Average time per adoption: {results['avg_time_per_adoption']} minutes")
        print(f"   • Non-adopting visitor percentage: {results['non_adopting_percentage']}%")
        print(f"   • Peak adoption hour: {results['peak_hour']}:00 ({results['peak_adoptions']} adoptions)")
        
        print(f"\n👥 COUNSELOR WORKLOAD:")
        print(f"   • Number of counselors: {results['num_counselors']}")
        print(f"   • Total daily counselor time needed: {results['total_counselor_hours']:.1f} hours")
        print(f"   • Average hours per counselor: {results['hours_per_counselor']:.1f} hours")
        print(f"   • Peak hour workload per counselor: {results['peak_hour_per_counselor']:.1f} hours")
        
        # Capacity analysis
        capacity_utilization = (results['hours_per_counselor'] / 8) * 100
        print(f"\n📈 CAPACITY ANALYSIS:")
        print(f"   • Daily capacity utilization: {capacity_utilization:.1f}%")
        
        if capacity_utilization < 80:
            status = "🟢 UNDER-UTILIZED"
        elif capacity_utilization < 100:
            status = "🟡 OPTIMAL"
        else:
            status = "🔴 OVER-CAPACITY"
        
        print(f"   • Status: {status}")
        
        if capacity_utilization > 100:
            additional_hours = results['hours_per_counselor'] - 8
            additional_counselors = additional_hours / 8
            print(f"   • Additional counselor time needed: {additional_hours:.1f} hours")
            print(f"   • Recommended additional counselors: {additional_counselors:.1f}")
        
        print("\n" + "="*60)


def main():
    """Main function to run the adoption forecast tool."""
    print("🐾 ADOPTION DEMAND FORECAST TOOL 🐾")
    print("="*50)
    
    # Get input file path
    csv_file = input("Enter the path to your CSV file: ").strip()
    
    try:
        # Initialize the forecast tool
        forecast = AdoptionForecast(csv_file)
        
        # Create visualizations
        print("\n📊 Creating visualizations...")
        daily_data = forecast.plot_adoptions_per_day()
        hourly_data = forecast.plot_adoptions_per_hour(plot_type='density')
        
        # Show distribution with filters
        print("\n📈 Creating distribution analysis...")
        forecast.plot_adoption_distribution()
        
        # Get user inputs
        print("\n⚙️  CONFIGURATION SETTINGS")
        print("-" * 30)
        
        avg_time = float(input("Enter average time per adoption (minutes): "))
        non_adopting_pct = float(input("Enter percentage of non-adopting visitors (0-100): "))
        num_counselors = int(input("Enter number of counselors working: "))
        
        # Calculate counselor needs
        print("\n🧮 Calculating counselor needs...")
        results = forecast.calculate_counselor_needs(avg_time, non_adopting_pct, num_counselors)
        
        # Print summary report
        forecast.print_summary_report(results)
        
        # Create capacity summary visualization
        print("\n📊 Creating capacity summary visualization...")
        forecast.plot_counselor_capacity_summary(results)
        
        print("\n✅ Analysis complete! Check the generated visualizations above.")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file}' not found.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 