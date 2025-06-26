#!/usr/bin/env python3
"""
Streamlit Web Interface for Adoption Demand Forecast Tool
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
from scipy import stats
import warnings
import os
warnings.filterwarnings('ignore')

# Import the main forecast class
from forecast import AdoptionForecast

def main():
    st.set_page_config(
        page_title="Adoption Demand Forecast",
        page_icon="🐾",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🐾 Adoption Demand Forecast Tool")
    st.markdown("---")
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Check if AnimalOutcome.csv exists
    csv_file = "AnimalOutcome.csv"
    
    if not os.path.exists(csv_file):
        st.error(f"❌ File '{csv_file}' not found in the current directory.")
        st.info("Please ensure AnimalOutcome.csv is in the same folder as this app.")
        return
    
    try:
        # Initialize forecast tool
        forecast = AdoptionForecast(csv_file)
        
        # Configuration section
        col1, col2 = st.sidebar.columns(2)
        with col1:
            avg_time = st.number_input(
                "Avg time per adoption (min)",
                min_value=5,
                max_value=120,
                value=30,
                step=5
            )
        
        with col2:
            non_adopting_pct = st.number_input(
                "Non-adopting visitors (%)",
                min_value=0.0,
                max_value=100.0,
                value=30.0,
                step=5.0
            )
        
        num_counselors = st.sidebar.number_input(
            "Number of counselors",
            min_value=1,
            max_value=20,
            value=3,
            step=1
        )
        
        # Show data info
        st.sidebar.markdown("---")
        st.sidebar.markdown("📊 **Data Info:**")
        st.sidebar.markdown(f"• Total records: {len(forecast.data):,}")
        st.sidebar.markdown(f"• Date range: {forecast.data['DateTime'].min().strftime('%Y-%m-%d')} to {forecast.data['DateTime'].max().strftime('%Y-%m-%d')}")
        st.sidebar.markdown(f"• Species: {', '.join(forecast.data['Species'].unique())}")
        
        # Main content area
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview", "📈 Trends", "⏰ Hourly Analysis", "👥 Counselor Analysis"
        ])
        
        with tab1:
            st.header("📊 Data Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Adoptions", len(forecast.data))
            
            with col2:
                st.metric("Date Range", f"{forecast.data['DateTime'].min().strftime('%Y-%m-%d')} to {forecast.data['DateTime'].max().strftime('%Y-%m-%d')}")
            
            with col3:
                avg_daily = forecast.data.groupby('Date').size().mean()
                st.metric("Avg Daily Adoptions", f"{avg_daily:.1f}")
            
            with col4:
                species_count = len(forecast.data['Species'].unique())
                st.metric("Species Types", species_count)
            
            # Species breakdown
            st.subheader("Species Breakdown")
            species_counts = forecast.data['Species'].value_counts()
            fig_species = px.pie(
                values=species_counts.values,
                names=species_counts.index,
                title="Adoptions by Species"
            )
            st.plotly_chart(fig_species, use_container_width=True)
            
            # Daily adoptions bell curve
            st.subheader("Daily Adoptions Distribution")
            daily_adoptions = forecast.data.groupby('Date').size()
            
            fig_bell = go.Figure()
            
            # Add histogram
            fig_bell.add_trace(go.Histogram(
                x=daily_adoptions.values,
                nbinsx=20,
                name='Actual Data',
                opacity=0.7,
                marker_color='skyblue'
            ))
            
            # Add fitted normal distribution
            mean_daily = daily_adoptions.mean()
            std_daily = daily_adoptions.std()
            x_smooth = np.linspace(daily_adoptions.min(), daily_adoptions.max(), 100)
            y_smooth = stats.norm.pdf(x_smooth, mean_daily, std_daily) * len(daily_adoptions) * (daily_adoptions.max() - daily_adoptions.min()) / 20
            
            fig_bell.add_trace(go.Scatter(
                x=x_smooth,
                y=y_smooth,
                mode='lines',
                name='Fitted Normal Distribution',
                line=dict(color='red', width=2)
            ))
            
            fig_bell.update_layout(
                title='Distribution of Daily Adoptions (Bell Curve)',
                xaxis_title='Number of Adoptions per Day',
                yaxis_title='Frequency',
                showlegend=True
            )
            
            st.plotly_chart(fig_bell, use_container_width=True)
            
            # Data preview at bottom
            st.subheader("Data Preview")
            st.dataframe(forecast.data.head(10))
        
        with tab2:
            st.header("📈 Trends")
            
            # Daily trends
            st.subheader("Daily Adoption Trends")
            daily_adoptions = forecast.data.groupby('Date').size().reset_index(name='Adoptions')
            
            fig_daily = px.line(
                daily_adoptions,
                x='Date',
                y='Adoptions',
                title='Adoptions per Day',
                markers=True
            )
            fig_daily.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Adoptions"
            )
            st.plotly_chart(fig_daily, use_container_width=True)
            
            # Daily statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Daily", f"{daily_adoptions['Adoptions'].mean():.1f}")
            with col2:
                st.metric("Max Daily", f"{daily_adoptions['Adoptions'].max()}")
            with col3:
                st.metric("Min Daily", f"{daily_adoptions['Adoptions'].min()}")
            
            # Monthly trends
            st.subheader("Monthly Trends")
            monthly_dist = forecast.data.groupby(['Year', 'Month']).size().reset_index(name='Adoptions')
            monthly_dist['Date'] = pd.to_datetime(monthly_dist[['Year', 'Month']].assign(day=1))
            
            fig_monthly = px.line(
                monthly_dist,
                x='Date',
                y='Adoptions',
                title='Adoptions per Month',
                markers=True
            )
            fig_monthly.update_layout(
                xaxis_title="Month",
                yaxis_title="Number of Adoptions"
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        with tab3:
            st.header("⏰ Hourly Adoption Analysis")
            
            # Day of week filter - in correct order
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            available_days = ['All Days'] + [day for day in day_order if day in forecast.data['DayOfWeek'].unique()]
            
            filter_day = st.selectbox(
                "Filter by Day of Week",
                available_days
            )
            
            # Apply filter
            filtered_data = forecast.data.copy()
            if filter_day != 'All Days':
                filtered_data = filtered_data[filtered_data['DayOfWeek'] == filter_day]
            
            if len(filtered_data) > 0:
                # Calculate TRUE average adoptions per hour for the filtered data
                # Include all days, even those with 0 adoptions at a given hour
                
                # Get all unique dates in the filtered data
                all_dates = filtered_data['Date'].unique()
                
                # Create a complete dataset with all date-hour combinations
                all_hours = range(24)
                complete_data = []
                
                for date in all_dates:
                    for hour in all_hours:
                        # Count adoptions for this specific date and hour
                        count = len(filtered_data[(filtered_data['Date'] == date) & (filtered_data['Hour'] == hour)])
                        complete_data.append({
                            'Date': date,
                            'Hour': hour,
                            'Adoptions': count
                        })
                
                # Convert to DataFrame and calculate true averages
                complete_df = pd.DataFrame(complete_data)
                hourly_adoptions = complete_df.groupby('Hour')['Adoptions'].mean().reset_index()
                
                # Create density plot
                fig_hourly = go.Figure()
                
                # Convert hours to 12-hour format for display
                def format_hour(hour):
                    if hour == 0:
                        return "12 AM"
                    elif hour < 12:
                        return f"{hour} AM"
                    elif hour == 12:
                        return "12 PM"
                    else:
                        return f"{hour - 12} PM"
                
                # Create hour labels for display
                hour_labels = [format_hour(h) for h in hourly_adoptions['Hour']]
                
                # Add bar chart
                fig_hourly.add_trace(go.Bar(
                    x=hour_labels,
                    y=hourly_adoptions['Adoptions'],
                    name='Average Adoptions',
                    marker_color='skyblue',
                    opacity=0.7
                ))
                
                title_suffix = f" - {filter_day}" if filter_day != 'All Days' else ""
                fig_hourly.update_layout(
                    title=f'Average Adoptions per Hour{title_suffix}',
                    xaxis_title='Hour of Day',
                    yaxis_title='Average Number of Adoptions',
                    showlegend=True
                )
                
                st.plotly_chart(fig_hourly, use_container_width=True)
                
                # Peak hour analysis
                peak_hour = hourly_adoptions.loc[hourly_adoptions['Adoptions'].idxmax()]
                peak_hour_formatted = format_hour(int(peak_hour['Hour']))
                st.info(f"📈 Peak adoption hour: {peak_hour_formatted} with {peak_hour['Adoptions']:.1f} average adoptions")
                
                # Show some context about the calculation
                total_days = len(all_dates)
                st.caption(f"📊 Based on {total_days} total days in the selected period")
            else:
                st.warning("No data matches the selected filter.")
        
        with tab4:
            st.header("👥 Counselor Workload Analysis")
            
            # Filters for counselor analysis
            col1, col2 = st.columns(2)
            with col1:
                # Day of week filter - in correct order
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                available_days_counselor = ['All'] + [day for day in day_order if day in forecast.data['DayOfWeek'].unique()]
                
                filter_day_counselor = st.selectbox(
                    "Filter by Day of Week",
                    available_days_counselor,
                    key="counselor_day_filter"
                )
            
            with col2:
                # Month filter with month names
                month_names = {
                    1: 'January', 2: 'February', 3: 'March', 4: 'April',
                    5: 'May', 6: 'June', 7: 'July', 8: 'August',
                    9: 'September', 10: 'October', 11: 'November', 12: 'December'
                }
                available_months = ['All'] + [month_names[month] for month in sorted(forecast.data['Month'].unique())]
                
                filter_month_counselor = st.selectbox(
                    "Filter by Month",
                    available_months,
                    key="counselor_month_filter"
                )
            
            # Apply filters
            filtered_data_counselor = forecast.data.copy()
            if filter_day_counselor != 'All':
                filtered_data_counselor = filtered_data_counselor[filtered_data_counselor['DayOfWeek'] == filter_day_counselor]
            if filter_month_counselor != 'All':
                # Convert month name back to number for filtering
                month_number = [k for k, v in month_names.items() if v == filter_month_counselor][0]
                filtered_data_counselor = filtered_data_counselor[filtered_data_counselor['Month'] == month_number]
            
            if len(filtered_data_counselor) > 0:
                # Calculate average daily adoptions for filtered data
                daily_adoptions_filtered = filtered_data_counselor.groupby('Date').size()
                avg_daily_adoptions_filtered = daily_adoptions_filtered.mean()
                
                # Override option
                st.subheader("📊 Workload Calculation")
                
                col1, col2 = st.columns(2)
                with col1:
                    use_override = st.checkbox("Override average adoptions with custom value")
                
                with col2:
                    if use_override:
                        override_adoptions = st.number_input(
                            "Custom daily adoptions",
                            min_value=1.0,
                            max_value=100.0,
                            value=float(avg_daily_adoptions_filtered),
                            step=1.0,
                            format="%.1f"
                        )
                        daily_adoptions_for_calc = override_adoptions
                    else:
                        daily_adoptions_for_calc = avg_daily_adoptions_filtered
                
                # Calculate counselor needs
                total_adoption_time = daily_adoptions_for_calc * avg_time  # minutes
                non_adopting_multiplier = 1 + (non_adopting_pct / 100)
                total_counselor_time = total_adoption_time * non_adopting_multiplier
                total_counselor_hours = total_counselor_time / 60
                hours_per_counselor = total_counselor_hours / num_counselors
                
                # Calculate expected guests
                expected_adopting_guests = daily_adoptions_for_calc
                expected_non_adopting_guests = daily_adoptions_for_calc * (non_adopting_pct / 100)
                total_expected_guests = expected_adopting_guests + expected_non_adopting_guests
                
                # Display math breakdown
                st.subheader("🧮 Calculation Breakdown")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Expected Guests:**")
                    st.markdown(f"• Adopting guests: {expected_adopting_guests:.1f}")
                    st.markdown(f"• Non-adopting guests: {expected_non_adopting_guests:.1f}")
                    st.markdown(f"• **Total expected guests: {total_expected_guests:.1f}**")
                    
                    st.markdown("**Time Calculation:**")
                    st.markdown(f"• Total time: {total_expected_guests:.1f} guests × {avg_time} min = {total_counselor_time:.0f} min")
                    st.markdown(f"• Convert to hours: {total_counselor_time:.0f} min ÷ 60 = {total_counselor_hours:.1f} hours")
                    st.markdown(f"• Per counselor: {total_counselor_hours:.1f} hours ÷ {num_counselors} counselors = **{hours_per_counselor:.1f} hours**")
                
                with col2:
                    # Peak day analysis (using 35 as peak)
                    peak_day_adoptions = 35
                    peak_day_adopting_guests = peak_day_adoptions
                    peak_day_non_adopting_guests = peak_day_adoptions * (non_adopting_pct / 100)
                    peak_day_total_guests = peak_day_adopting_guests + peak_day_non_adopting_guests
                    peak_day_total_time = peak_day_total_guests * avg_time / 60  # hours
                    peak_day_per_counselor = peak_day_total_time / num_counselors
                    
                    st.markdown("**Peak Day Analysis (35 adoptions):**")
                    st.markdown(f"• Adopting guests: {peak_day_adopting_guests:.1f}")
                    st.markdown(f"• Non-adopting guests: {peak_day_non_adopting_guests:.1f}")
                    st.markdown(f"• **Total expected guests: {peak_day_total_guests:.1f}**")
                    st.markdown("**Time Calculation:**")
                    st.markdown(f"• Total time: {peak_day_total_guests:.1f} guests × {avg_time} min = {peak_day_total_guests * avg_time:.0f} min")
                    st.markdown(f"• Convert to hours: {peak_day_total_guests * avg_time:.0f} min ÷ 60 = {peak_day_total_time:.1f} hours")
                    st.markdown(f"• Per counselor: {peak_day_total_time:.1f} hours ÷ {num_counselors} counselors = **{peak_day_per_counselor:.1f} hours**")
                
                # Workload summary chart
                st.subheader("📈 Workload Summary")
                
                # Create workload breakdown including full workday
                workday_hours = 7  # 11 AM to 6 PM
                total_workday_time = workday_hours * num_counselors
                
                breakdown_data = {
                    'Category': ['Adoption Time', 'Non-Adoption Time', 'Available Time'],
                    'Hours': [
                        total_adoption_time / 60,
                        (total_counselor_time - total_adoption_time) / 60,
                        total_workday_time - total_counselor_hours
                    ]
                }
                
                breakdown_df = pd.DataFrame(breakdown_data)
                
                # Create two columns for side-by-side display
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_breakdown = px.pie(
                        breakdown_df,
                        values='Hours',
                        names='Category',
                        title='Daily Time Breakdown (7-hour workday)'
                    )
                    st.plotly_chart(fig_breakdown, use_container_width=True)
                
                with col2:
                    # Hourly workload distribution - using the same calculation as hourly analysis tab
                    if len(filtered_data_counselor) > 0:
                        # Get all unique dates in the filtered data
                        all_dates_counselor = filtered_data_counselor['Date'].unique()
                        
                        # Create a complete dataset with all date-hour combinations
                        all_hours = range(24)
                        complete_data_counselor = []
                        
                        for date in all_dates_counselor:
                            for hour in all_hours:
                                # Count adoptions for this specific date and hour
                                count = len(filtered_data_counselor[(filtered_data_counselor['Date'] == date) & (filtered_data_counselor['Hour'] == hour)])
                                complete_data_counselor.append({
                                    'Date': date,
                                    'Hour': hour,
                                    'Adoptions': count
                                })
                        
                        # Convert to DataFrame and calculate true averages
                        complete_df_counselor = pd.DataFrame(complete_data_counselor)
                        hourly_adoptions_counselor = complete_df_counselor.groupby('Hour')['Adoptions'].mean()
                        
                        # Calculate workload
                        hourly_workload = hourly_adoptions_counselor * avg_time * non_adopting_multiplier / 60
                        
                        # Convert hours to 12-hour format for display
                        def format_hour(hour):
                            if hour == 0:
                                return "12 AM"
                            elif hour < 12:
                                return f"{hour} AM"
                            elif hour == 12:
                                return "12 PM"
                            else:
                                return f"{hour - 12} PM"
                        
                        # Create hour labels for display
                        hour_labels_workload = [format_hour(h) for h in hourly_workload.index]
                        
                        fig_hourly_workload = go.Figure()
                        fig_hourly_workload.add_trace(go.Bar(
                            x=hour_labels_workload,
                            y=hourly_workload.values,
                            name='Total Workload (hours)',
                            marker_color='lightcoral'
                        ))
                        
                        # Add per-counselor line
                        fig_hourly_workload.add_hline(
                            y=hours_per_counselor,
                            line_dash="dash",
                            line_color="green",
                            annotation_text=f"Average per counselor ({hours_per_counselor:.1f} hrs)"
                        )
                        
                        # Add workday line
                        fig_hourly_workload.add_hline(
                            y=workday_hours,
                            line_dash="dash",
                            line_color="red",
                            annotation_text=f"Workday limit ({workday_hours} hrs)"
                        )
                        
                        fig_hourly_workload.update_layout(
                            title='Hourly Workload Distribution',
                            xaxis_title='Hour of Day',
                            yaxis_title='Total Workload (hours)',
                            showlegend=True
                        )
                        
                        st.plotly_chart(fig_hourly_workload, use_container_width=True)
            
            else:
                st.warning("No data matches the selected filters.")
    
    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.info("Please ensure your CSV file has the required columns: Outcome, AnimalNumber, Species, DateTime")

if __name__ == "__main__":
    main() 