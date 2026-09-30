import ReactMarkdown from "react-markdown";

function AIReport({ aiReport }) {
  if (!aiReport) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 animate-float-in">
      <div className="prose prose-invert max-w-none text-slate-300">
        <ReactMarkdown>
          {aiReport}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default AIReport;