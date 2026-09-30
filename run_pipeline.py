from src.pipeline import run_insightflow_pipeline
from src.reporting import display_results

from src.visualizer import (
    generate_all_categorical_charts,
    create_bar_chart
)

DATASET_PATH = "data/sales.csv"


def main():
    report = run_insightflow_pipeline(DATASET_PATH)

    display_results(report)


    print("\nCharts Saved At:")
    for path in report["eda_report"]["chart_paths"]:
        print("-", path)


if __name__ == "__main__":
    main()