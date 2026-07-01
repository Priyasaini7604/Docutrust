import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

// Upload PDF to backend
export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE}/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

// Ask question to CRAG pipeline
export const askQuestion = async (question) => {
  const response = await axios.post(`${API_BASE}/ask`, { question });
  return response.data;
};