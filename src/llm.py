def build_qa_prompt(report, question):
    dataset_summary = report["eda_report"]["dataset_summary"]

    cleaning_report = report["cleaning_report"]

    numerical_summary = report["eda_report"]["numerical_summary"]

    categorical_summary = report["eda_report"]["categorical_summary"]

    ai_insights = report["eda_report"]["ai_insights"]

    prompt = f"""
You are an expert AI Data Analyst.

Use only the provided report information.
Do not invent values or assumptions.

Dataset Summary:
{dataset_summary}

Cleaning Report:
{cleaning_report}

Numerical Summary:
{numerical_summary}

Categorical Summary:
{categorical_summary}

Existing Insights:
{ai_insights}

User Question:
{question}

Provide a professional and structured answer.
"""

    return prompt