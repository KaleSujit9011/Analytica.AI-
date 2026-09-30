def format_chat_history(chat_history):
    if not chat_history:
        return "No previous conversation."

    formatted_history = ""

    for message in chat_history:
        role = message["role"]
        content = message["message"]

        formatted_history += f"{role.title()}: {content}\n\n"

    return formatted_history


def build_qa_prompt(report, question, chat_history):
    dataset_summary = report["eda_report"]["dataset_summary"]
    cleaning_report = report["cleaning_report"]
    numerical_summary = report["eda_report"]["numerical_summary"]
    categorical_summary = report["eda_report"]["categorical_summary"]
    ai_insights = report["eda_report"]["ai_insights"]

    formatted_history = format_chat_history(chat_history)

    prompt = f"""
You are an expert AI Data Analyst.

Answer the user's current question using only:
1. The provided report context
2. The previous conversation history

Do not invent values, dates, company names, or assumptions.

Report Context:

Dataset Summary:
{dataset_summary}

Cleaning Report:
{cleaning_report}

Numerical Summary:
{numerical_summary}

Categorical Summary:
{categorical_summary}

Existing AI Insights:
{ai_insights}

Previous Conversation:
{formatted_history}

Current User Question:
{question}

Give a clear, professional, and helpful answer.
"""

    return prompt