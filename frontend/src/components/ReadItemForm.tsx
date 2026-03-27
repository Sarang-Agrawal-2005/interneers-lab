import React, { useState } from "react";
import "./Form.css";

interface Props {
  type: "products" | "categories";
}

function ReadItemForm({ type }: Props) {
  const [id, setId] = useState("");
  const [result, setResult] = useState<any>(null);

  async function handleRead() {
    const response = await fetch(`http://localhost:8000/api/${type}/${id}`);

    const data = await response.json();
    setResult(data);
  }

  return (
    <div className="form">
      <input
        placeholder={`Enter ${type === "products" ? "SKU" : "Category ID"}`}
        onChange={(e) => setId(e.target.value)}
      />
      <button onClick={handleRead}>Fetch</button>

      {result && (
        <pre className="result-box">{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}

export default ReadItemForm;
