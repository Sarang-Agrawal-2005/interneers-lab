import React, { useState } from "react";
import "./Form.css";

function CreateCategoryForm() {
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
      "http://localhost:8000/api/categories/create/",
      {
        method: "POST",
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
        name="title"
        placeholder="Title"
        required
        onChange={handleChange}
      />
      <input
        name="description"
        placeholder="Description"
        required
        onChange={handleChange}
      />

      <button type="submit">Create Category</button>
    </form>
  );
}

export default CreateCategoryForm;
