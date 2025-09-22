import React, { useEffect, useRef, useState } from "react";

const SpeechInput = ({ onResult }) => {
  const recognitionRef = useRef(null);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.error("Web Speech API is not supported in this browser.");
      setError("Speech recognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      console.log(" Speech recognition started");
      setTranscript("");
      setError("");
    };

    recognition.onresult = (event) => {
      const text = Array.from(event.results).map((r) => r[0].transcript).join("");
      console.log(" Transcript:", text);
      setTranscript(text);
      onResult(text);
    };

    recognition.onerror = (event) => {
      console.error(" Speech recognition error:", event.error);
      if (event.error === "no-speech") setError("No speech detected — try again.");
      else if (event.error === "network") setError("Network issue — check your connection.");
      else if (event.error === "not-allowed") setError("Microphone blocked — allow mic access.");
      else setError("Speech error occurred. Please try again.");
    };

    recognition.onend = () => {
      console.log("⛔ Speech recognition ended");
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  }, [onResult]);

  const toggleListening = () => {
    if (!recognitionRef.current) return;
    if (isListening) recognitionRef.current.stop();
    else recognitionRef.current.start();
    setIsListening((prev) => !prev);
  };

  return (
    <div style={{ marginBottom: 10 }}>
      <button
        onClick={toggleListening}
        style={{
          backgroundColor: isListening ? "#ffcccc" : "#d4edda",
          color: "#333",
          border: "none",
          padding: "10px 15px",
          borderRadius: 8,
          cursor: "pointer",
        }}
      >
        {isListening ? " Listening..." : " Start Talking"}
      </button>
      {transcript && (
        <div style={{ marginTop: 5, fontStyle: "italic", color: "#555" }}>
          You said: "{transcript}"
        </div>
      )}
      {error && (
        <div style={{ marginTop: 4, color: "#b94a48" }}>
          {error}
        </div>
      )}
    </div>
  );
};

export default SpeechInput;
