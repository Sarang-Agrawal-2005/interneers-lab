import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ProductPage.css";

interface Product {
  sku: number;
  name: string;
  brand: string;
  category_id: string;
  reorder_level: number;
  quantity: number;
}

function ProductPage() {
  const { productId } = useParams(); // SKU from URL
  const navigate = useNavigate();

  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  // Fetch product details
  useEffect(() => {
    fetch(`http://localhost:8000/api/products/${productId}/`)
      .then((res) => {
        if (!res.ok) throw new Error("Product not found");
        return res.json();
      })
      .then((data) => {
        setProduct(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to fetch product");
        setLoading(false);
      });
  }, [productId]);

  // Handle form changes
  const updateField = (field: keyof Product, value: string | number) => {
    if (!product) return;
    setProduct({ ...product, [field]: value });
  };

  // Save changes (PUT)
  const saveProduct = async () => {
    if (!product) return;
    setSaving(true);
    setError("");

    try {
      const res = await fetch(
        `http://localhost:8000/api/products/update/${productId}/`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(product),
        },
      );

      if (!res.ok) throw new Error("Failed to save product");

      alert("Product updated successfully!");
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  // Delete product
  const deleteProduct = async () => {
    const yes = window.confirm("Are you sure you want to delete this product?");
    if (!yes) return;

    try {
      const res = await fetch(
        `http://localhost:8000/api/products/delete/${productId}/`,
        { method: "DELETE" },
      );

      if (!res.ok) throw new Error("Failed to delete product");

      alert("Product deleted successfully!");
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message);
    }
  };

  // UI Rendering
  if (loading) return <p className="loading">Loading product...</p>;
  if (error) return <p className="error">{error}</p>;
  if (!product) return <p>No product found.</p>;

  return (
    <div className="product-page">
      <h1>Edit Product: {product.name}</h1>

      <div className="form-container">
        <label>
          Name:
          <input
            type="text"
            value={product.name}
            onChange={(e) => updateField("name", e.target.value)}
          />
        </label>

        <label>
          Brand:
          <input
            type="text"
            value={product.brand}
            onChange={(e) => updateField("brand", e.target.value)}
          />
        </label>

        <label>
          Category:
          <input
            type="text"
            value={product.category_id}
            onChange={(e) => updateField("category_id", e.target.value)}
          />
        </label>

        <label>
          Reorder Level:
          <input
            type="number"
            value={product.reorder_level}
            onChange={(e) =>
              updateField("reorder_level", Number(e.target.value))
            }
          />
        </label>

        <label>
          Quantity:
          <input
            type="number"
            value={product.quantity}
            onChange={(e) => updateField("quantity", Number(e.target.value))}
          />
        </label>

        {error && <p className="error">{error}</p>}

        <div className="button-row">
          <button onClick={saveProduct} disabled={saving}>
            {saving ? "Saving..." : "Save Changes"}
          </button>

          <button className="delete-btn" onClick={deleteProduct}>
            Delete Product
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProductPage;
