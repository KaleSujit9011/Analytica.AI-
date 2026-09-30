import { useParams, Link } from "react-router-dom";
import Layout from "../components/Layout";
import DatasetChat from "../components/DatasetChat";

function ChatPage() {
  const { reportId } = useParams();

  return (
    <Layout>
      <div className="animate-float-in">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">
              Dataset Chat
            </h1>

            <p className="text-slate-400 mt-2">
              Chatting with report: {reportId}
            </p>
          </div>

          <Link
            to={`/report/${reportId}`}
            className="px-5 py-3 rounded-xl bg-slate-800 text-white font-bold hover:bg-slate-700 transition"
          >
            View AI Report
          </Link>
        </div>

        <DatasetChat reportId={reportId} />
      </div>
    </Layout>
  );
}

export default ChatPage;