def build_report_prompt(report):
    cleaning_report = report["cleaning_report"]

    dataset_summary = report["eda_report"]["dataset_summary"]

    numerical_summary = report["eda_report"]["numerical_summary"]

    categorical_summary = report["eda_report"]["categorical_summary"]

    ai_insights = report["eda_report"]["ai_insights"]

    chart_paths = report["eda_report"]["chart_paths"]

    prompt = f"""
You are a senior data analyst.

Create a professional business-style data analysis report.
Do not add fake dates, author names, company names, or assumptions.
Use only the provided information.

Dataset Summary:
{dataset_summary}

Cleaning Report:
{cleaning_report}

Numerical Summary:
{numerical_summary}

Categorical Summary:
{categorical_summary}

AI Insights:
{ai_insights}

Generated Charts:
{chart_paths}

Generate a structured report with:

1. Executive Summary
2. Dataset Overview
3. Data Quality Assessment
4. Key Findings
5. Business Insights
6. Recommendations

Write professionally and clearly.
"""

    return prompt