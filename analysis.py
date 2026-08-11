from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).parent
DATA = BASE / "data" / "shipments.csv"
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

REQUIRED_COLUMNS = {
    "shipment_id", "ship_date", "destination", "carrier",
    "planned_days", "actual_days", "status", "weight_kg"
}


def load_and_validate(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")
    if df["ship_date"].isna().any():
        raise ValueError("Invalid ship_date values found")

    if df["shipment_id"].duplicated().any():
        raise ValueError("Duplicate shipment_id values found")

    return df


def build_analysis(df: pd.DataFrame) -> None:
    delivered = df[df["status"] == "Delivered"].copy()
    delivered["delay_days"] = delivered["actual_days"] - delivered["planned_days"]
    delivered["on_time"] = delivered["delay_days"] <= 0
    delivered["month"] = delivered["ship_date"].dt.to_period("M").astype(str)

    total_shipments = len(df)
    delivered_shipments = len(delivered)
    delayed_open = int((df["status"] == "Delayed").sum())
    in_transit = int((df["status"] == "In Transit").sum())
    on_time_rate = delivered["on_time"].mean() * 100 if delivered_shipments else 0
    avg_delay = delivered.loc[delivered["delay_days"] > 0, "delay_days"].mean()
    avg_delay = 0 if pd.isna(avg_delay) else avg_delay

    kpis = pd.DataFrame({
        "metric": [
            "total_shipments", "delivered_shipments", "open_delayed_shipments",
            "in_transit_shipments", "on_time_rate_pct",
            "avg_delay_days_when_late", "total_weight_kg"
        ],
        "value": [
            total_shipments, delivered_shipments, delayed_open, in_transit,
            round(on_time_rate, 1), round(avg_delay, 2), int(df["weight_kg"].sum())
        ]
    })
    kpis.to_csv(OUT / "kpi_summary.csv", index=False)

    carrier = (
        delivered.groupby("carrier")
        .agg(
            delivered_shipments=("shipment_id", "count"),
            avg_delay_days=("delay_days", "mean"),
            on_time_rate_pct=("on_time", "mean")
        )
        .reset_index()
    )
    carrier["on_time_rate_pct"] = (carrier["on_time_rate_pct"] * 100).round(1)
    carrier["avg_delay_days"] = carrier["avg_delay_days"].round(2)
    carrier = carrier.sort_values("on_time_rate_pct", ascending=False)
    carrier.to_csv(OUT / "carrier_performance.csv", index=False)

    destination = (
        delivered.groupby("destination")
        .agg(
            delivered_shipments=("shipment_id", "count"),
            avg_delay_days=("delay_days", "mean"),
            on_time_rate_pct=("on_time", "mean")
        )
        .reset_index()
    )
    destination["on_time_rate_pct"] = (destination["on_time_rate_pct"] * 100).round(1)
    destination["avg_delay_days"] = destination["avg_delay_days"].round(2)
    destination = destination.sort_values("on_time_rate_pct", ascending=False)
    destination.to_csv(OUT / "destination_performance.csv", index=False)

    monthly = (
        delivered.groupby("month")
        .agg(
            delivered_shipments=("shipment_id", "count"),
            on_time_rate_pct=("on_time", "mean"),
            avg_delay_days=("delay_days", "mean")
        )
        .reset_index()
    )
    monthly["on_time_rate_pct"] = (monthly["on_time_rate_pct"] * 100).round(1)
    monthly["avg_delay_days"] = monthly["avg_delay_days"].round(2)
    monthly.to_csv(OUT / "monthly_performance.csv", index=False)

    plt.figure(figsize=(8, 4.5))
    plt.bar(carrier["carrier"], carrier["on_time_rate_pct"])
    plt.title("On-time delivery rate by carrier")
    plt.ylabel("On-time rate (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(OUT / "carrier_on_time_rate.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 4.5))
    plt.plot(monthly["month"], monthly["on_time_rate_pct"], marker="o")
    plt.title("Monthly on-time delivery rate")
    plt.xlabel("Month")
    plt.ylabel("On-time rate (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(OUT / "monthly_on_time_trend.png", dpi=160)
    plt.close()

    best_carrier = carrier.iloc[0]
    weakest_carrier = carrier.iloc[-1]
    best_destination = destination.iloc[0]
    weakest_destination = destination.iloc[-1]

    insights = f"""# Analysis Summary\n\nThis portfolio project uses synthetic shipment data.\n\n## Executive KPIs\n- Total shipments: {total_shipments}\n- Delivered shipments: {delivered_shipments}\n- Currently delayed: {delayed_open}\n- In transit: {in_transit}\n- On-time rate for completed deliveries: {on_time_rate:.1f}%\n- Average delay when a completed shipment is late: {avg_delay:.2f} days\n- Total transported weight: {int(df['weight_kg'].sum()):,} kg\n\n## Operational observations\n- Best carrier by on-time rate: {best_carrier['carrier']} ({best_carrier['on_time_rate_pct']:.1f}%).\n- Lowest carrier on-time rate: {weakest_carrier['carrier']} ({weakest_carrier['on_time_rate_pct']:.1f}%).\n- Best destination by on-time rate: {best_destination['destination']} ({best_destination['on_time_rate_pct']:.1f}%).\n- Lowest destination on-time rate: {weakest_destination['destination']} ({weakest_destination['on_time_rate_pct']:.1f}%).\n\n## Business interpretation\nThe dashboard can be used as a lightweight operational monitoring layer. A real-world next step would be to connect the same KPI logic to a production data source and investigate late deliveries by carrier, destination, route, and time period.\n"""
    (OUT / "analysis_summary.md").write_text(insights, encoding="utf-8")

    print(kpis.to_string(index=False))
    print("\nCarrier performance:\n", carrier.to_string(index=False))
    print("\nMonthly performance:\n", monthly.to_string(index=False))
    print(f"\nSaved outputs to: {OUT}")


if __name__ == "__main__":
    build_analysis(load_and_validate(DATA))
