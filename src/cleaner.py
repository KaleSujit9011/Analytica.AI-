import pandas as pd

def fix_column_names(df):
    cleaned_df = df.copy()

    new_columns = []

    for column in cleaned_df.columns:
        fixed_column = column.strip().lower().replace(" ", "_")
        new_columns.append(fixed_column)

    cleaned_df.columns = new_columns

    return cleaned_df


def remove_duplicates(df):
    before_rows = len(df)

    cleaned_df = df.drop_duplicates()

    after_rows = len(cleaned_df)

    duplicate_count = before_rows - after_rows

    return cleaned_df, duplicate_count


def handle_missing_values(df):
    cleaned_df = df.copy()

    before_filling = cleaned_df.isnull().sum().sum()

    for column in cleaned_df.columns:
        if pd.api.types.is_numeric_dtype(cleaned_df[column]):
            q1 = cleaned_df[column].quantile(0.25)
            q3 = cleaned_df[column].quantile(0.75)
            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            mask = (cleaned_df[column] < lower_bound) | (cleaned_df[column] > upper_bound)
            outliers = cleaned_df[column][mask].tolist()

            if outliers:
                fill_value = cleaned_df[column].median()
            else:
                fill_value = cleaned_df[column].mean()

            cleaned_df[column] = cleaned_df[column].fillna(fill_value)

        else:
            cleaned_df[column] = cleaned_df[column].fillna("Unknown")

    after_filling = cleaned_df.isnull().sum().sum()
    missing_values_filled = before_filling - after_filling

    return cleaned_df, missing_values_filled


def convert_data_types(df):
    cleaned_df = df.copy()

    for column in cleaned_df.columns:

        if pd.api.types.is_float_dtype(cleaned_df[column]):

            integer_checks = []

            for value in cleaned_df[column]:
                integer_checks.append(value.is_integer())

            if all(integer_checks):
                cleaned_df[column] = cleaned_df[column].astype(int)

    return cleaned_df


def detect_outliers(df):
    cleaned_df = df.copy()
    outlier_report = []

    for column in cleaned_df.columns:
        if pd.api.types.is_numeric_dtype(cleaned_df[column]):
            q1 = cleaned_df[column].quantile(0.25)
            q3 = cleaned_df[column].quantile(0.75)
            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            mask = (cleaned_df[column] < lower_bound) | (cleaned_df[column] > upper_bound)
            outliers = cleaned_df[column][mask].tolist()

            if outliers:
                outlier_report.append({
                    "column": column,
                    "outliers": outliers,
                    "lower_bound": lower_bound,
                    "upper_bound": upper_bound
                })

    return outlier_report

