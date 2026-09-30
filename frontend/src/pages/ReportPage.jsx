import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import Layout from "../components/Layout";
import AIReport from "../components/AIReport";
import { generateAIReport } from "../api";

function ReportPage() {
  const { reportId } = useParams();
  const [aiReport, setAiReport] = useState("");
  const [loading, setLoading] = useState(false);
  const [pdfAvailable, setPdfAvailable] = useState(false);

  useEffect(() => {
    loadAIReport();
  }, [reportId]);

  const loadAIReport = async () => {
    try {
      setLoading(true);

      const result = await generateAIReport(reportId);

      console.log("AI Report Response:", result);

      const reportText =
        result?.ai_report?.content ||
        result?.ai_report?.response ||
        result?.ai_report?.error ||
        result?.error ||
        "AI report could not be generated.";

      setAiReport(reportText);

      if (result?.ai_report?.pdf_path) {
        setPdfAvailable(true);
      }
    } catch (error) {
      console.error(error);
      alert("Failed to generate AI report.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="animate-float-in">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">
              AI Report
            </h1>

            <p className="text-slate-400 mt-2">
              Report ID: {reportId}
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <Link
              to={`/chat/${reportId}`}
              className="px-5 py-3 rounded-xl bg-cyan-500 text-slate-950 font-bold hover:bg-cyan-400 transition"
            >
              Chat With This Dataset
            </Link>

            {pdfAvailable && (
              <a
                href={`${import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}/reports/${reportId}/download-ai-report-pdf`}
                className="px-5 py-3 rounded-xl bg-emerald-500 text-slate-950 font-bold hover:bg-emerald-400 transition"
              >
                Download PDF
              </a>
            )}
          </div>
        </div>

        {loading && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-slate-300">
            Loading AI report...
          </div>
        )}

        <AIReport aiReport={aiReport} />
      </div>
    </Layout>
  );
}

export default ReportPage;