import pandas as pd

from src.cleaner import (
    fix_column_names,
    remove_duplicates,
    handle_missing_values,
    convert_data_types,
    detect_outliers,
)

from src.eda import (
    generate_dataset_summary,
    generate_numerical_summary,
    generate_categorical_summary,
    generate_ai_insights,
)

from src.visualizer import (
    generate_all_categorical_charts,
    create_bar_chart,
    generate_all_numeric_box_plots,
    create_box_plot,
)


def detect_encoding(file_path):
    """Detect file encoding by checking BOM markers, with fallbacks."""
    with open(file_path, "rb") as f:
        raw = f.read(4)

    if raw[:2] == b"\xff\xfe":
        return "utf-16"
    if raw[:2] == b"\xfe\xff":
        return "utf-16"
    if raw[:3] == b"\xef\xbb\xbf":
        return "utf-8-sig"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            while f.read(1024 * 1024):
                pass
    except UnicodeDecodeError:
        return "latin-1"

    return "utf-8"


def run_cleaning_pipeline(df):
    cleaned_df = fix_column_names(df)

    cleaned_df, duplicate_count = remove_duplicates(cleaned_df)

    cleaned_df, missing_values_filled = handle_missing_values(cleaned_df)

    cleaned_df = convert_data_types(cleaned_df)

    outlier_report = detect_outliers(cleaned_df)

    cleaning_report = {
        "duplicates_removed": duplicate_count,
        "missing_values_filled": missing_values_filled,
        "outlier_report": outlier_report,
    }

    return cleaned_df, cleaning_report


def run_eda_pipeline(cleaned_df, outlier_report):
    dataset_summary = generate_dataset_summary(cleaned_df)
    numerical_summary = generate_numerical_summary(cleaned_df)
    categorical_summary = generate_categorical_summary(cleaned_df)

    ai_insights = generate_ai_insights(
        dataset_summary,
        numerical_summary,
        categorical_summary,
        outlier_report,
    )

    categorical_chart_configs = generate_all_categorical_charts(
        categorical_summary
    )

    chart_paths = []

    for chart_config in categorical_chart_configs:
        chart_path = create_bar_chart(chart_config)
        chart_paths.append(chart_path)

    box_plot_configs = generate_all_numeric_box_plots(
        numerical_summary
    )

    for chart_config in box_plot_configs:
        chart_path = create_box_plot(
            chart_config,
            cleaned_df
        )
        chart_paths.append(chart_path)

    eda_report = {
        "dataset_summary": dataset_summary,
        "numerical_summary": numerical_summary,
        "categorical_summary": categorical_summary,
        "ai_insights": ai_insights,
        "chart_paths": chart_paths,
    }

    return eda_report


def run_insightflow_pipeline(file_path):
    df = pd.read_csv(file_path, encoding=detect_encoding(file_path))

    cleaned_df, cleaning_report = run_cleaning_pipeline(df)

    eda_report = run_eda_pipeline(
        cleaned_df,
        cleaning_report["outlier_report"],
    )

    final_report = {
        "cleaned_df": cleaned_df,
        "cleaning_report": cleaning_report,
        "eda_report": eda_report,
    }

    return final_report