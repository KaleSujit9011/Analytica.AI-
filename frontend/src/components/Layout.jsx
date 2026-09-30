import { Link, useLocation } from "react-router-dom";

function Layout({ children }) {
  const location = useLocation();

  const navItems = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Reports", path: "/reports" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white flex">
      <aside className="hidden md:flex w-72 bg-slate-900/80 border-r border-slate-800 p-6 flex-col">
        <div>
          <h1 className="text-2xl font-bold text-cyan-400">
            InsightFlow AI
          </h1>
          <p className="text-sm text-slate-400 mt-2">
            AI Data Analyst Platform
          </p>
        </div>

        <nav className="mt-10 space-y-3">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`block px-4 py-3 rounded-xl transition ${
                location.pathname === item.path
                  ? "bg-cyan-500 text-slate-950 font-semibold"
                  : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              {item.name}
            </Link>
          ))}
        </nav>

        <div className="mt-auto text-xs text-slate-500">
          Built with FastAPI, React, Pandas & Gemini
        </div>
      </aside>

      <main className="flex-1 p-5 md:p-8 overflow-x-hidden">
        {children}
      </main>
    </div>
  );
}

export default Layout;