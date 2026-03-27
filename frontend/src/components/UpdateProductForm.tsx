import React, { useState } from "react";
import "./Form.css";

function UpdateProductForm() {
  const [sku, setSku] = useState("");
  const [formData, setFormData] = useState({});

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const response = await fetch(
      `http://localhost:8000/api/products/update/${sku}/`,
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
        placeholder="Enter SKU to update"
        required
        onChange={(e) => setSku(e.target.value)}
      />

      <input name="name" placeholder="Name" onChange={handleChange} />
      <input
        name="quantity"
        type="number"
        placeholder="Quantity"
        onChange={handleChange}
      />
      <input
        name="reorder_level"
        type="number"
        placeholder="Reorder Level"
        onChange={handleChange}
      />
      <input
        name="category_id"
        placeholder="Category ID"
        onChange={handleChange}
      />
      <input name="brand" placeholder="Brand" onChange={handleChange} />

      <button type="submit">Update Product</button>
    </form>
  );
}

export default UpdateProductForm;
