import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,#0891b255,transparent_35%),radial-gradient(circle_at_bottom_left,#22d3ee33,transparent_35%)]" />

      <main className="relative z-10 min-h-screen flex items-center justify-center px-6">
        <div className="max-w-5xl text-center animate-float-in">
          <p className="text-cyan-400 font-semibold mb-4">
            AI-Powered Data Analyst
          </p>

          <h1 className="text-5xl md:text-7xl font-extrabold leading-tight">
            Turn messy CSV data into
            <span className="text-cyan-400"> insights, charts, and AI reports.</span>
          </h1>

          <p className="text-slate-300 text-lg md:text-xl mt-6 max-w-3xl mx-auto">
            InsightFlow AI cleans datasets, performs EDA, generates visualizations,
            writes professional AI reports, and lets you chat with your data.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/dashboard"
              className="px-8 py-4 bg-cyan-500 text-slate-950 rounded-2xl font-bold hover:bg-cyan-400 transition"
            >
              Get Started
            </Link>

            <Link
              to="/reports"
              className="px-8 py-4 bg-slate-900 border border-slate-700 rounded-2xl font-bold hover:bg-slate-800 transition"
            >
              View Reports
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-16">
            {[
              "Automated Data Cleaning",
              "EDA & Charts",
              "Gemini AI Reports",
              "Chat With Dataset",
            ].map((feature) => (
              <div
                key={feature}
                className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5"
              >
                <p className="text-cyan-400 font-bold">✓</p>
                <p className="mt-2 text-slate-300">{feature}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default Home;