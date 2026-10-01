"""Fetch product inventory data and generate inventory reports."""

from pathlib import Path

import requests

from api_client import InventoryAPIClient, InventoryReportGenerator


def main() -> None:
    """Retrieve inventory data, process it, and export report files."""
    output_directory = Path("reports")
    output_directory.mkdir(parents=True, exist_ok=True)

    api_client = InventoryAPIClient()

    try:
        products = api_client.fetch_all_products()
    except requests.RequestException as error:
        print(f"Unable to retrieve inventory data: {error}")
        return
    finally:
        api_client.session.close()

    report_generator = InventoryReportGenerator(products)
    report_generator.process_inventory(low_stock_threshold=10)

    csv_path = output_directory / "inventory_report.csv"
    summary_path = output_directory / "summary_metrics.json"

    report_generator.export_csv(csv_path)
    report_generator.export_summary_metrics(summary_path)

    print(f"Inventory report generated: {csv_path}")
    print(f"Summary metrics generated: {summary_path}")


if __name__ == "__main__":
    main()
