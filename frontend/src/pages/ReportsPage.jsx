import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Layout from "../components/Layout";
import { getReports } from "../api";

function ReportsPage() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      const result = await getReports();

      const cleanReports = result.filter(
        (report) => !report.report_id.includes("_chat")
      );

      setReports(cleanReports);
    } catch (error) {
      console.error(error);
      alert("Failed to load reports.");
    }
  };

  return (
    <Layout>
      <div className="animate-float-in">
        <h1 className="text-4xl font-bold text-cyan-400">
          Reports
        </h1>

        <p className="text-slate-400 mt-2">
          View previous dataset analyses and continue working with them.
        </p>

        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
          {reports.length === 0 && (
            <p className="text-slate-400">
              No reports found yet.
            </p>
          )}

          {reports.map((report) => (
            <div
              key={report.report_id}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-cyan-500/60 transition"
            >
              <h2 className="text-xl font-bold text-white">
                {report.report_id}
              </h2>

              <p className="text-slate-500 text-sm mt-2">
                {report.report_path}
              </p>

              <div className="flex gap-3 mt-6">
                <Link
                  to={`/report/${report.report_id}`}
                  className="px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-bold hover:bg-cyan-400 transition"
                >
                  Report
                </Link>

                <Link
                  to={`/chat/${report.report_id}`}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-white font-bold hover:bg-slate-700 transition"
                >
                  Chat
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}

export default ReportsPage;