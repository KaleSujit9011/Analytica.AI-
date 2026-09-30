import pandas as pd


def generate_dataset_summary(df):
    rows, columns = df.shape

    column_names = df.columns.tolist()

    numeric_columns = []

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            numeric_columns.append(column)

    categorical_columns = []

    for column in column_names:
        if column not in numeric_columns:
            categorical_columns.append(column)

    summary = {
        "rows": rows,
        "columns": columns,
        "column_names": column_names,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns
    }

    return summary


def generate_numerical_summary(df):
    numerical_summary = {}

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            numerical_summary[column] = {
                "count": int(df[column].count()),
                "min": float(df[column].min()),
                "max": float(df[column].max()),
                "mean": float(df[column].mean()),
                "median": float(df[column].median())
            }

    return numerical_summary


import pandas as pd


def generate_categorical_summary(df):
    categorical_summary = {}

    for column in df.columns:
        if not pd.api.types.is_numeric_dtype(df[column]):

            frequency = df[column].value_counts().to_dict()

            unique_values = int(df[column].nunique())

            max_frequency = max(frequency.values())

            most_common = []

            for value, count in frequency.items():
                if count == max_frequency:
                    most_common.append(value)

            categorical_summary[column] = {
                "unique_values": unique_values,
                "most_common": most_common,
                "frequency": frequency
            }

    return categorical_summary


def generate_ai_insights(dataset_summary, numerical_summary, categorical_summary, outlier_report):
    insights = []

    # 1. Dataset size insight
    rows = dataset_summary["rows"]
    columns = dataset_summary["columns"]

    insights.append({
        "type": "dataset_summary",
        "message": f"The dataset contains {rows} rows and {columns} columns."
    })

    # 2. Outlier insights
    for item in outlier_report:
        column = item["column"]
        outliers = item["outliers"]
        outlier_count = len(outliers)

        insights.append({
            "type": "outlier",
            "message": f"The '{column}' column contains {outlier_count} potential outlier(s): {outliers}."
        })

    # 3. Distribution insights
    for column, stats in numerical_summary.items():
        mean = stats["mean"]
        median = stats["median"]

        if median != 0 and mean > median * 2:
            insights.append({
                "type": "distribution",
                "message": (
                    f"The '{column}' column appears highly skewed. "
                    f"The mean ({mean}) is much higher than the median ({median}), "
                    f"which may indicate extreme values."
                )
            })

    # 4. Categorical insights
    for column, summary in categorical_summary.items():
        unique_values = summary["unique_values"]
        most_common = summary["most_common"]

        insights.append({
            "type": "categorical",
            "message": f"The '{column}' column contains {unique_values} unique value(s)."
        })

        if len(most_common) > 1:
            insights.append({
                "type": "categorical",
                "message": (
                    f"No single dominant value exists in the '{column}' column. "
                    f"Multiple values share the highest frequency: {most_common}."
                )
            })
        else:
            insights.append({
                "type": "categorical",
                "message": f"The most common value in '{column}' is '{most_common[0]}'."
            })

    return {
        "insights": insights
    }