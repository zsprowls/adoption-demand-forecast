adoption-demand-forecast

A Python-based forecasting tool that analyzes shelter adoption data and estimates daily counselor time needs based on adoption patterns, estimated interaction time, and staff capacity.

---

##Purpose

This tool helps shelter leadership:
- Visualize adoption trends by day, time, and species
- Understand peak times and workload distribution
- Estimate how long adoption counseling takes per day
- Forecast counselor capacity vs. daily demand
- Justify wait times and staffing strategies with data

---

##Features

Load historical adoption data (AnimalNumber, Species, DateTime)  
Graph daily and hourly adoption patterns  
Show bell curve/distribution of adoption timing  
Filter by day of the week  
Estimate time per adoption  
Account for non-adopting visitors who require similar time  
Input number of counselors to calculate workload per staff member  
Highlight peak time pressure points

---

##How It Works

You provide:
- A CSV with adoption records (with datetime of each)
- Your estimates for:
  - Time per adoption (e.g. 30 min)
  - % of visitors who don’t adopt (e.g. 30%)
  - Number of counselors scheduled

The tool outputs:
- Total projected counselor time needed per day
- Per-counselor workload breakdown
- Visuals to identify peaks, bottlenecks, and quiet periods

---

##File Format Requirements

Upload a CSV with the following columns:
- `Outcome`: Always "Adoption"
- `AnimalNumber`: Unique animal ID
- `Species`: Dog, Cat, etc.
- `DateTime`: When the adoption happened (`e.g. 6/26/24 8:34`)

---

##Planned Visuals

- Daily adoption count over time
- Hourly adoption heatmap
- Distribution curve (with min/max)
- Filters by weekday and species
- Counselor workload summary graph

---

##Getting Started

```bash
git clone https://github.com/your-username/adoption-demand-forecast.git
cd adoption-demand-forecast
pip install -r requirements.txt
python forecast.py
