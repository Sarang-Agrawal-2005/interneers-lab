import React, { useState } from "react";
import "./Form.css";

function DeleteItemForm({ type }: { type: "products" | "categories" }) {
  const [id, setId] = useState("");

  async function handleDelete() {
    const response = await fetch(
      `http://localhost:8000/api/${type}/delete/${id}/`,
      {
        method: "DELETE",
      },
    );

    alert(`Deleted ${type.slice(0, -1)} with id ${id}`);
  }

  return (
    <div className="form">
      <input
        placeholder={`Enter ${type === "products" ? "SKU" : "Category ID"}`}
        onChange={(e) => setId(e.target.value)}
      />
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}

export default DeleteItemForm;
