import { useState, useEffect } from "react";
import { askQuestion, getChatHistory } from "../api";
import ReactMarkdown from "react-markdown";

function DatasetChat({ reportId }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadChatHistory();
  }, [reportId]);

 const loadChatHistory = async () => {
  try {
    const result = await getChatHistory(reportId);

    console.log("Chat History Response:", result);

    const chatHistory = result?.chat_history || [];

    const formattedMessages = chatHistory.map((message) => ({
      role: message.role,
      text: message.message,
    }));

    setMessages(formattedMessages);
  } catch (error) {
    console.error(error);
  }
};

  const handleAsk = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);
      const currentQuestion = question;

      const result = await askQuestion(reportId, currentQuestion);

      setMessages((prevMessages) => [
        ...prevMessages,
        { role: "user", text: currentQuestion },
        { role: "assistant", text: result.answer },
      ]);

      setQuestion("");
    } catch (error) {
      console.error(error);
      alert("Failed to get answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 animate-float-in">
      <h2 className="text-2xl font-bold text-cyan-400">
        Chat With Dataset
      </h2>

      <p className="text-slate-400 mt-2">
        Ask questions about this report. The assistant uses report context and chat memory.
      </p>

      <div className="mt-6 space-y-5 max-h-[520px] overflow-y-auto pr-2">
        {messages.length === 0 && (
          <p className="text-slate-500">
            No messages yet. Ask your first question.
          </p>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`rounded-2xl p-4 ${
              message.role === "user"
                ? "bg-cyan-500 text-slate-950 ml-auto max-w-3xl"
                : "bg-slate-950 border border-slate-800 text-slate-300 mr-auto max-w-3xl"
            }`}
          >
            <p className="font-bold mb-2">
              {message.role === "user" ? "You" : "InsightFlow AI"}
            </p>

            <ReactMarkdown>
              {message.text}
            </ReactMarkdown>
          </div>
        ))}

        {loading && (
          <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 text-slate-400">
            Thinking...
          </div>
        )}
      </div>

      <div className="mt-6 flex gap-3">
        <input
          type="text"
          placeholder="Ask a question about your dataset..."
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          disabled={loading}
          className="flex-1 px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-white outline-none focus:border-cyan-500"
        />

        <button
          onClick={handleAsk}
          disabled={loading}
          className="px-6 py-3 rounded-xl bg-cyan-500 text-slate-950 font-bold hover:bg-cyan-400 transition disabled:opacity-60"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>
    </div>
  );
}

export default DatasetChat;