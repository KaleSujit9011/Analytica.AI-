import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import ReportPage from "./pages/ReportPage";
import ChatPage from "./pages/ChatPage";
import ReportsPage from "./pages/ReportsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/report/:reportId" element={<ReportPage />} />
        <Route path="/chat/:reportId" element={<ChatPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;