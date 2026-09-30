function StatCard({ title, value }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 hover:border-cyan-500/60 transition animate-float-in">
      <p className="text-slate-400 text-sm">{title}</p>
      <h3 className="text-3xl font-bold text-white mt-2">{value}</h3>
    </div>
  );
}

function AnalysisReport({ report }) {
  if (!report) return null;

  const datasetSummary = report.eda_report.dataset_summary;
  const cleaningReport = report.cleaning_report;
  const aiInsights = report.eda_report.ai_insights.insights;
  const chartPaths = report.eda_report.chart_paths;

  return (
    <div className="mt-10 space-y-8">
      <section>
        <h2 className="text-2xl font-bold text-white mb-4">
          Dataset Overview
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <StatCard title="Rows" value={datasetSummary.rows} />
          <StatCard title="Columns" value={datasetSummary.columns} />
          <StatCard title="Duplicates Removed" value={cleaningReport.duplicates_removed} />
          <StatCard title="Missing Values Filled" value={cleaningReport.missing_values_filled} />
        </div>
      </section>

      <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 animate-float-in">
        <h2 className="text-2xl font-bold text-cyan-400 mb-4">
          AI Insights
        </h2>

        <div className="space-y-4">
          {aiInsights.map((insight, index) => (
            <div
              key={index}
              className="bg-slate-950 border border-slate-800 rounded-xl p-4"
            >
              <p className="text-cyan-400 font-semibold capitalize">
                {insight.type}
              </p>
              <p className="text-slate-300 mt-1">
                {insight.message}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold text-white mb-4">
          Visualizations
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {chartPaths.map((path, index) => (
            <div
              key={index}
              className="bg-white rounded-2xl p-4 animate-float-in"
            >
              <img
                src={`${import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}/${path}`}
                alt={`Chart ${index + 1}`}
                className="w-full rounded-xl"
              />
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default AnalysisReport;