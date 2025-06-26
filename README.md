# Adoption Demand Forecast Tool

A comprehensive Python-based forecasting tool that analyzes shelter adoption data and estimates daily counselor time needs based on adoption patterns, estimated interaction time, and staff capacity.

## 🎯 Purpose

This tool helps shelter leadership:
- Visualize adoption trends by day, time, and species
- Understand peak times and workload distribution
- Estimate how long adoption counseling takes per day
- Forecast counselor capacity vs. daily demand
- Justify wait times and staffing strategies with data

## ✨ Features

- **Data Analysis**: Load and process CSV files with adoption records
- **Visualizations**: 
  - Daily adoption trends with trend lines
  - Hourly adoption patterns with density plots (bell curves)
  - Distribution analysis with filtering by day of week and species
  - Counselor capacity vs. workload summary graphs
- **Forecasting**: Calculate total counselor time needs and per-counselor workload
- **Interactive Interface**: Streamlit web app for easy data upload and analysis
- **Modular Design**: Clean, readable code structure with separate modules

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/adoption-demand-forecast.git
cd adoption-demand-forecast

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Sample Data (Optional)

```bash
# Generate sample data for testing
python generate_sample_data.py
```

This creates two sample CSV files:
- `sample_adoption_data.csv` - Standard adoption patterns
- `sample_weekend_data.csv` - Weekend-heavy adoption patterns

### 3. Run the Tool

#### Option A: Command Line Interface
```bash
python forecast.py
```
Then follow the prompts to enter your CSV file path and configuration settings.

#### Option B: Streamlit Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```
Then open your browser to the provided URL and upload your CSV file.

## 📁 File Format Requirements

Your CSV file must have these columns:
- `Outcome`: Always "Adoption"
- `AnimalNumber`: Unique animal ID (e.g., "A001", "A002")
- `Species`: Animal species (e.g., "Dog", "Cat", "Other")
- `DateTime`: When the adoption happened (format: "6/26/24 8:34")

### Example CSV:
```csv
Outcome,AnimalNumber,Species,DateTime
Adoption,A001,Dog,6/26/24 8:34
Adoption,A002,Cat,6/26/24 14:22
Adoption,A003,Dog,6/27/24 10:15
```

## 📊 Analysis Features

### 1. Daily Trends
- Line chart showing adoptions per day
- Trend line to identify overall patterns
- Statistics on average, maximum, and minimum daily adoptions

### 2. Hourly Analysis
- Bar chart with fitted normal distribution curve
- Peak hour identification
- Density plot showing adoption time patterns

### 3. Distribution Analysis
- Filterable by day of week and species
- Four-panel visualization:
  - Hourly distribution
  - Day of week distribution
  - Species breakdown (pie chart)
  - Monthly trends

### 4. Counselor Workload Analysis
- Total daily counselor time calculation
- Per-counselor workload breakdown
- Capacity utilization analysis
- Peak hour workload assessment
- Recommendations for staffing adjustments

## ⚙️ Configuration Parameters

When running the tool, you'll need to provide:

1. **Average Time per Adoption** (minutes): How long each adoption typically takes
   - Typical range: 20-45 minutes
   - Default: 30 minutes

2. **Non-Adopting Visitors Percentage** (0-100%): Percentage of visitors who don't adopt but still require counselor time
   - Typical range: 20-50%
   - Default: 30%

3. **Number of Counselors**: How many adoption counselors are working
   - Typical range: 1-10
   - Default: 3

## 📈 Output Analysis

The tool provides:

### Key Metrics
- Total daily counselor hours needed
- Average hours per counselor
- Capacity utilization percentage
- Peak hour workload per counselor

### Capacity Assessment
- 🟢 **UNDER-UTILIZED** (<80%): Counselors have capacity for additional workload
- 🟡 **OPTIMAL** (80-100%): Workload is well-balanced
- 🔴 **OVER-CAPACITY** (>100%): Additional counselors may be needed

### Visualizations
- Comprehensive dashboard with multiple charts
- Interactive plots (in Streamlit version)
- Export-ready visualizations

## 🏗️ Project Structure

```
adoption-demand-forecast/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── forecast.py              # Main analysis script
├── streamlit_app.py         # Streamlit web interface
├── generate_sample_data.py  # Sample data generator
├── sample_adoption_data.csv # Generated sample data
└── sample_weekend_data.csv  # Weekend-heavy sample data
```

## 🔧 Technical Details

### Dependencies
- **pandas**: Data manipulation and analysis
- **matplotlib**: Static plotting
- **plotly**: Interactive plotting
- **streamlit**: Web interface
- **numpy**: Numerical computations
- **seaborn**: Statistical visualizations
- **scipy**: Statistical functions

### Key Classes
- `AdoptionForecast`: Main analysis class with methods for:
  - Data loading and preprocessing
  - Visualization generation
  - Counselor workload calculations
  - Capacity analysis

## 🎯 Use Cases

### For Shelter Managers
- **Staffing Decisions**: Determine optimal number of counselors
- **Schedule Planning**: Identify peak hours for better scheduling
- **Resource Allocation**: Understand workload distribution

### For Operations Teams
- **Wait Time Management**: Predict busy periods
- **Capacity Planning**: Ensure adequate counselor coverage
- **Performance Analysis**: Track adoption patterns over time

### For Leadership
- **Budget Planning**: Justify staffing requests with data
- **Strategic Planning**: Understand seasonal and weekly patterns
- **Reporting**: Generate data-driven reports for stakeholders

## 🚨 Troubleshooting

### Common Issues

1. **CSV Format Errors**
   - Ensure your CSV has the exact column names: `Outcome`, `AnimalNumber`, `Species`, `DateTime`
   - Check that DateTime format is consistent (e.g., "6/26/24 8:34")

2. **Installation Issues**
   - Make sure you're using Python 3.7+
   - Try: `pip install --upgrade pip` before installing requirements

3. **Streamlit Issues**
   - If Streamlit doesn't start, try: `streamlit run streamlit_app.py --server.port 8501`

### Getting Help
- Check the sample data format in `sample_adoption_data.csv`
- Run `python generate_sample_data.py` to create test data
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Made with ❤️ for animal shelters everywhere**
