const BASE_URL = process.env.REACT_APP_API_BASE || "http://127.0.0.1:5000";

export const sendMessage = async (message) => {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error("Chat API error");
  return await res.json();
};

export const detectEmotion = async (message) => {
  const res = await fetch(`${BASE_URL}/emotion`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error("Emotion API error");
  return await res.json();
};
