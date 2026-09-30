def display_results(report):
    cleaned_df = report["cleaned_df"]
    cleaning_report = report["cleaning_report"]
    eda_report = report["eda_report"]

    print("\n========== CLEANING REPORT ==========")
    print("Duplicates Removed:", cleaning_report["duplicates_removed"])
    print("Missing Values Filled:", cleaning_report["missing_values_filled"])

    print("\n========== OUTLIER REPORT ==========")
    print(cleaning_report["outlier_report"])

    print("\n========== CLEANED DATASET ==========")
    print(cleaned_df)

    print("\n========== DATASET SUMMARY ==========")
    print(eda_report["dataset_summary"])

    print("\n========== NUMERICAL SUMMARY ==========")
    print(eda_report["numerical_summary"])

    print("\n========== CATEGORICAL SUMMARY ==========")
    print(eda_report["categorical_summary"])

    print("\n========== AI INSIGHTS ==========")
    for insight in eda_report["ai_insights"]["insights"]:
        print(f"- [{insight['type']}] {insight['message']}")