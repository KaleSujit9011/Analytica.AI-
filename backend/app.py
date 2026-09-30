import os
import shutil
import json
from datetime import datetime

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.pipeline import run_insightflow_pipeline
from src.report_generator import build_report_prompt
from src.gemini_service import call_gemini
from src.qa import build_qa_prompt
from src.pdf_generator import create_ai_report_pdf
from src.storage import (
    save_report,
    load_report,
    update_report,
    save_chat_message,
    load_chat_history,
    save_cleaned_dataset,
    save_outlier_removed_dataset,
)



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        os.getenv("FRONTEND_URL", "")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/charts",
    StaticFiles(directory="charts"),
    name="charts"
)

UPLOAD_FOLDER = "uploads"


@app.get("/")
def home():
    return {
        "message": "InsightFlow API is running"
    }



def convert_numpy_types(obj):
    if hasattr(obj, "item"):
        return obj.item()

    if isinstance(obj, dict):
        return {
            key: convert_numpy_types(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            convert_numpy_types(item)
            for item in obj
        ]

    return obj


@app.post("/analyze")
def analyze_dataset(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    report = run_insightflow_pipeline(file_path)

    report_for_json = report.copy()
    report_for_json["cleaned_df"] = report["cleaned_df"].to_dict(
        orient="records"
    )

    report_for_json = convert_numpy_types(report_for_json)

    saved_report = save_report(report_for_json)

    report_id = saved_report["report_id"]

    cleaned_dataset_path = save_cleaned_dataset(
        report["cleaned_df"],
        report_id
    )

    outlier_removed_dataset_path = save_outlier_removed_dataset(
        report["cleaned_df"],
        report["cleaning_report"]["outlier_report"],
        report_id
    )

    report_for_json["download_files"] = {
        "cleaned_dataset": cleaned_dataset_path,
        "outlier_removed_dataset": outlier_removed_dataset_path
    }

    report_for_json["saved_report"] = saved_report

    return report_for_json


@app.get("/reports")
def get_reports():
    reports_folder = "reports"

    reports = []

    if not os.path.exists(reports_folder):
        return reports

    for file_name in os.listdir(reports_folder):
        if file_name.endswith(".json"):
            report_id = file_name.replace(".json", "")

            reports.append(
                {
                    "report_id": report_id,
                    "report_path": f"reports/{file_name}"
                }
            )

    return reports


@app.get("/reports/{report_id}")
def get_report_by_id(report_id: str):
    file_path = f"reports/{report_id}.json"

    if not os.path.exists(file_path):
        return {
            "error": f"Report '{report_id}' not found."
        }

    with open(file_path, "r") as file:
        report = json.load(file)

    return report


class QuestionRequest(BaseModel):
    report_id: str
    question: str


@app.post("/ask")
def ask_question(request: QuestionRequest):
    report = load_report(request.report_id)

    if report is None:
        return {
            "error": f"Report '{request.report_id}' not found."
        }

    chat_history = load_chat_history(request.report_id)

    prompt = build_qa_prompt(
        report,
        request.question,
        chat_history
    )

    ai_answer = call_gemini(prompt)

    answer_text = ai_answer.get("response", "")

    save_chat_message(
        request.report_id,
        "user",
        request.question
    )

    save_chat_message(
        request.report_id,
        "assistant",
        answer_text
    )

    return {
        "report_id": request.report_id,
        "question": request.question,
        "answer": answer_text
    }


@app.get("/reports/{report_id}/chat")
def get_chat_history(report_id: str):

    report = load_report(report_id)

    if report is None:
        return {
            "error": f"Report '{report_id}' not found."
        }

    chat_history = load_chat_history(report_id)

    return {
        "report_id": report_id,
        "chat_history": chat_history
    }


@app.post("/reports/{report_id}/generate-ai-report")
def generate_ai_report(report_id: str):
    report = load_report(report_id)

    if report is None:
        return {
            "error": f"Report '{report_id}' not found."
        }

    if "ai_report" in report:
        return {
            "report_id": report_id,
            "ai_report": report["ai_report"],
            "cached": True
        }

    prompt = build_report_prompt(report)

    ai_response = call_gemini(prompt)

    if "error" in ai_response:
        return {
            "report_id": report_id,
            "ai_report": ai_response,
            "cached": False
        }

    ai_report_text = ai_response["response"]

    pdf_path = create_ai_report_pdf(
        report_id,
        ai_report_text
    )

    report["ai_report"] = {
        "content": ai_report_text,
        "pdf_path": pdf_path,
        "generated_at": datetime.now().isoformat()
    }

    update_report(report_id, report)

    return {
        "report_id": report_id,
        "ai_report": report["ai_report"],
        "cached": False
    }


@app.get("/reports/{report_id}/download-cleaned")
def download_cleaned_dataset(report_id: str):
    file_path = f"cleaned_data/{report_id}_cleaned.csv"

    if not os.path.exists(file_path):
        return {
            "error": "Cleaned dataset not found."
        }

    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=f"{report_id}_cleaned.csv"
    )


@app.get("/reports/{report_id}/download-no-outliers")
def download_outlier_removed_dataset(report_id: str):
    file_path = f"cleaned_data/{report_id}_no_outliers.csv"

    if not os.path.exists(file_path):
        return {
            "error": "Outlier removed dataset not found."
        }

    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=f"{report_id}_no_outliers.csv"
    )


@app.get("/reports/{report_id}/download-ai-report-pdf")
def download_ai_report_pdf(report_id: str):
    report = load_report(report_id)

    if report is None:
        return {
            "error": f"Report '{report_id}' not found."
        }

    if "ai_report" not in report:
        return {
            "error": "AI report has not been generated yet."
        }

    pdf_path = report["ai_report"].get("pdf_path")

    if not pdf_path or not os.path.exists(pdf_path):
        return {
            "error": "PDF report not found."
        }

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{report_id}_ai_report.pdf"
    )