# Logistics Operations Dashboard

A portfolio project that turns shipment records into operational KPIs for delivery performance, carrier reliability and delay monitoring.

> **Data note:** all shipment records in this repository are synthetic and created for portfolio/demo purposes.

## Why I built this
My professional background includes logistics coordination, operational reporting, incident handling and process improvement. I built this project to demonstrate how those operational skills can be combined with Python and data analysis to support data-driven decisions.

## Business questions
The analysis answers five practical questions:

1. How many shipments were delivered, delayed or remain in transit?
2. What percentage of completed deliveries arrived on time?
3. Which carriers have the strongest and weakest delivery performance?
4. Which destinations show higher operational risk?
5. How does on-time performance change month by month?

## Tech stack
- Python 3
- pandas
- matplotlib
- CSV data processing
- KPI design and operational analysis

## Project structure
```text
logistics-operations-dashboard/
├── analysis.py
├── requirements.txt
├── data/
│   └── shipments.csv
└── output/
    ├── analysis_summary.md
    ├── carrier_on_time_rate.png
    ├── carrier_performance.csv
    ├── destination_performance.csv
    ├── kpi_summary.csv
    ├── monthly_on_time_trend.png
    └── monthly_performance.csv
```

## Data quality checks
Before calculating KPIs, the script validates:
- required columns;
- shipment ID uniqueness;
- valid shipment dates.

## Key outputs
The script calculates:
- total shipments;
- delivered shipments;
- currently delayed shipments;
- shipments in transit;
- on-time delivery rate;
- average delay for late completed shipments;
- total transported weight;
- carrier performance;
- destination performance;
- monthly performance trend.

### Carrier performance
![Carrier on-time delivery rate](output/carrier_on_time_rate.png)

### Monthly trend
![Monthly on-time delivery rate](output/monthly_on_time_trend.png)

## How to run
```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies and run:
```bash
pip install -r requirements.txt
python analysis.py
```

Generated results are written to the `output/` folder.

## What this project demonstrates
- translating an operational problem into measurable KPIs;
- cleaning and validating structured data;
- grouping and aggregating data with pandas;
- building reusable analysis scripts;
- presenting results visually;
- interpreting technical output from a business perspective.

## Next improvements
- interactive dashboard using Power BI or Streamlit;
- route-level analysis;
- SLA thresholds and automated alerts;
- SQL database instead of CSV input;
- automated tests for KPI calculations.
