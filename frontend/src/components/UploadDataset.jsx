import { useState } from "react";
import { Link } from "react-router-dom";
import { analyzeDataset } from "../api";
import AnalysisReport from "./AnalysisReport";

function UploadDataset() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please select a CSV file.");
      return;
    }

    try {
      setLoading(true);

      const result = await analyzeDataset(file);

      setReport(result);
    } catch (error) {
      console.error(error);
      alert(error.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const reportId = report?.saved_report?.report_id;

  return (
    <div className="space-y-8">
      <section className="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-3xl p-8 animate-float-in">
        <div className="max-w-3xl">
          <p className="text-cyan-400 font-semibold">
            Dataset Upload
          </p>

          <h2 className="text-3xl font-bold mt-2">
            Upload your CSV and generate instant insights
          </h2>

          <p className="text-slate-400 mt-3">
            InsightFlow AI will clean your data, generate summaries,
            detect outliers, create charts, and prepare AI-powered insights.
          </p>
        </div>

        <div className="mt-8 flex flex-col md:flex-row gap-4 items-start md:items-center">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="block w-full md:w-auto text-sm text-slate-300
            file:mr-4 file:py-3 file:px-5 file:rounded-xl
            file:border-0 file:text-sm file:font-semibold
            file:bg-cyan-500 file:text-slate-950
            hover:file:bg-cyan-400"
          />

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="px-6 py-3 rounded-xl bg-cyan-500 text-slate-950 font-bold hover:bg-cyan-400 transition disabled:opacity-60"
          >
            {loading ? "Analyzing..." : "Analyze Dataset"}
          </button>
        </div>
      </section>

      <AnalysisReport report={report} />

      {reportId && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col gap-5 animate-float-in">
          <div>
            <h3 className="text-xl font-bold">
              Continue with this analysis
            </h3>

            <p className="text-slate-400 mt-1">
              Report ID: {reportId}
            </p>

            <p className="text-slate-500 text-sm mt-2">
              Generate a professional AI report, chat with this dataset,
              or download cleaned versions for ML training and other tasks.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <Link
              to={`/report/${reportId}`}
              className="px-5 py-3 rounded-xl bg-cyan-500 text-slate-950 font-bold hover:bg-cyan-400 transition"
            >
              Generate AI Report
            </Link>

            <Link
              to={`/chat/${reportId}`}
              className="px-5 py-3 rounded-xl bg-slate-800 text-white font-bold hover:bg-slate-700 transition"
            >
              Chat With Dataset
            </Link>

            <a
              href={`${import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}/reports/${reportId}/download-cleaned`}
              className="px-5 py-3 rounded-xl bg-emerald-500 text-slate-950 font-bold hover:bg-emerald-400 transition"
            >
              Download Cleaned CSV
            </a>

            <a
              href={`${import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}/reports/${reportId}/download-no-outliers`}
              className="px-5 py-3 rounded-xl bg-purple-500 text-white font-bold hover:bg-purple-400 transition"
            >
              Download No-Outliers CSV
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default UploadDataset;