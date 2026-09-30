import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const getFriendlyErrorMessage = (error) => {
  const status = error?.response?.status;

  if (status === 429) {
    return "AI API usage limit reached. Please try again after some time.";
  }

  if (status === 401 || status === 403) {
    return "AI service authentication failed. Please contact the project owner.";
  }

  if (status >= 500) {
    return "Server is temporarily unavailable. Please try again after some time.";
  }

  if (!error.response) {
    return "Unable to connect to the server. Please try again after some time.";
  }

  return "Something went wrong. Please try again.";
};

const handleApiError = (error) => {
  throw new Error(getFriendlyErrorMessage(error));
};

export const analyzeDataset = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

export const generateAIReport = async (reportId) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/reports/${reportId}/generate-ai-report`
    );

    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

export const askQuestion = async (reportId, question) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/ask`, {
      report_id: reportId,
      question: question,
    });

    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

export const getChatHistory = async (reportId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/reports/${reportId}/chat`);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

export const getReports = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/reports`);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};