import React, { useState } from "react";
import "./Form.css";

function UpdateCategoryForm() {
  const [categoryId, setCategoryId] = useState("");
  const [formData, setFormData] = useState({
    title: "",
    description: "",
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const response = await fetch(
      `http://localhost:8000/api/categories/update/${categoryId}/`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      },
    );

    const result = await response.json();
    alert(JSON.stringify(result, null, 2));
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <input
        placeholder="Enter Category ID"
        required
        onChange={(e) => setCategoryId(e.target.value)}
      />

      <input name="title" placeholder="New Title" onChange={handleChange} />

      <input
        name="description"
        placeholder="New Description"
        onChange={handleChange}
      />

      <button type="submit">Update Category</button>
    </form>
  );
}

export default UpdateCategoryForm;
