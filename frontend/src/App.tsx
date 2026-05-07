import { useEffect, useState } from "react";

export default function App() {
  const [message, setMessage] = useState("loading...");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function getMessage() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch("https://mathapplication.onrender.com/hello");

        if (!res.ok) {
          throw new Error(`HTTP error: ${res.status}`);
        }

        const data = await res.json();
        setMessage(data.message);
      } catch (err) {
        setError("failed to reach backend");
      } finally {
        setLoading(false);
      }
    }

    getMessage();
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>Backend Response</h1>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!loading && !error && <p>{message}</p>}
    </div>
  );
}