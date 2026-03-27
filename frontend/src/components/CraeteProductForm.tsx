import React, { useState } from "react";
import "./Form.css";

function CreateProductForm() {
  const [formData, setFormData] = useState({
    sku: "",
    name: "",
    quantity: "",
    reorder_level: "",
    category_id: "",
    brand: "",
  });

  const [result, setResult] = useState<any>(null);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/api/products/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const result = await response.json();
    alert(JSON.stringify(result, null, 2));
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <input
        name="sku"
        type="number"
        placeholder="SKU"
        required
        onChange={handleChange}
      />
      <input name="name" placeholder="Name" required onChange={handleChange} />
      <input
        name="quantity"
        type="number"
        placeholder="Quantity"
        required
        onChange={handleChange}
      />
      <input
        name="reorder_level"
        type="number"
        placeholder="Reorder Level"
        required
        onChange={handleChange}
      />
      <input
        name="category_id"
        placeholder="Category ID"
        onChange={handleChange}
      />
      <input
        name="brand"
        placeholder="Brand"
        required
        onChange={handleChange}
      />

      <button type="submit">Create Product</button>
    </form>
  );
}

export default CreateProductForm;
