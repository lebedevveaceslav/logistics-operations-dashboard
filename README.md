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
├── sample_output.txt
├── data/
│   └── shipments.csv
└── output/
    ├── analysis_summary.md
    ├── carrier_performance.csv
    ├── destination_performance.csv
    ├── kpi_summary.csv
    └── monthly_performance.csv
```

## Data quality checks
Before calculating KPIs, the script validates:
- required columns;
- shipment ID uniqueness;
- valid shipment dates.

## Key results

| KPI | Result |
|---|---:|
| Total shipments | 120 |
| Delivered shipments | 74 |
| Currently delayed | 24 |
| In transit | 22 |
| On-time delivery rate | 70.3% |
| Average delay when late | 1.50 days |
| Total transported weight | 87,391 kg |

### Carrier performance

| Carrier | Delivered | Avg. delay | On-time rate |
|---|---:|---:|---:|
| NorthLine | 23 | 0.17 days | 82.6% |
| MoldCargo | 32 | 0.44 days | 71.9% |
| RapidTrans | 19 | 0.79 days | 52.6% |

### Operational observations
- NorthLine has the strongest on-time performance in the demo dataset at **82.6%**.
- RapidTrans has the lowest on-time performance at **52.6%**.
- Balti is the strongest destination by on-time rate at **84.6%**.
- Cahul has the lowest destination on-time rate at **50.0%**.
- Monthly on-time performance ranges from **66.7% to 73.3%** across the three-month demo period.

The Python script also generates two PNG charts locally when executed: carrier on-time delivery rate and monthly on-time delivery trend.

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
