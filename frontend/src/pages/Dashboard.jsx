import Layout from "../components/Layout";
import UploadDataset from "../components/UploadDataset";

function Dashboard() {
  return (
    <Layout>
      <div className="animate-float-in">
        <h1 className="text-4xl font-bold text-cyan-400">
          Dashboard
        </h1>

        <p className="text-slate-400 mt-2">
          Upload a dataset, generate insights, create AI reports,
          and chat with your data.
        </p>

        <div className="mt-8">
          <UploadDataset />
        </div>
      </div>
    </Layout>
  );
}

export default Dashboard;