import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generate_bar_chart(categorical_summary, column_name):
    if column_name not in categorical_summary:
        return {
            "error": f"Column '{column_name}' not found."
        }

    frequency = categorical_summary[column_name]["frequency"]
    title = column_name.title() + " Frequency"

    return {
        "chart_type": "bar",
        "title": title,
        "data": frequency
    }


def generate_all_categorical_charts(categorical_summary):
    chart_configs = []

    for column_name in categorical_summary:
        chart_config = generate_bar_chart(
            categorical_summary,
            column_name
        )

        chart_configs.append(chart_config)

    return chart_configs


def create_bar_chart(chart_config, output_folder="charts"):
    if "error" in chart_config:
        return chart_config

    os.makedirs(output_folder, exist_ok=True)

    data = chart_config["data"]

    x_values = list(data.keys())
    y_values = list(data.values())

    chart_title = chart_config["title"]

    file_name = chart_title.lower().replace(" ", "_") + ".png"

    chart_path = os.path.join(
        output_folder,
        file_name
    )

    plt.figure(figsize=(8, 5))

    plt.bar(x_values, y_values)

    plt.title(chart_title)
    plt.xlabel("Category")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(chart_path)

    plt.close()

    return chart_path.replace("\\", "/")


def generate_box_plot_config(numerical_summary, column_name):
    if column_name not in numerical_summary:
        return {
            "error": f"Column '{column_name}' not found."
        }

    title = column_name.title() + " Box Plot"

    return {
        "chart_type": "box_plot",
        "title": title,
        "column_name": column_name
    }


def generate_all_numeric_box_plots(numerical_summary):
    chart_configs = []

    for column_name in numerical_summary:
        chart_config = generate_box_plot_config(
            numerical_summary,
            column_name
        )

        chart_configs.append(chart_config)

    return chart_configs


def create_box_plot(chart_config, cleaned_df, output_folder="charts"):
    if "error" in chart_config:
        return chart_config

    os.makedirs(output_folder, exist_ok=True)

    column_name = chart_config["column_name"]
    chart_title = chart_config["title"]

    file_name = chart_title.lower().replace(" ", "_") + ".png"
    chart_path = os.path.join(output_folder, file_name)

    plt.figure(figsize=(8, 5))
    plt.boxplot(cleaned_df[column_name])
    plt.title(chart_title)
    plt.ylabel(column_name.title())
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path.replace("\\", "/")