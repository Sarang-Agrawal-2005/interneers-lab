import React, { useEffect, useState } from "react";
import "./ProductDashboard.css";

function ProductDashboard({ page }: { page: "products" | "categories" }) {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8000/api/${page}/`)
      .then((res) => res.json())
      .then((data) => setItems(data))
      .catch((err) => console.error(err));
  }, [page]);

  return (
    <div className="product-dashboard">
      {items.length === 0 ? (
        <p className="loading-text">Loading {page}...</p>
      ) : page === "products" ? (
        /* ---------- PRODUCT CARDS ---------- */
        <div className="product-grid">
          {items.map((item: any) => (
            <div className="product-card" key={item.sku}>
              <h3 className="product-title">{item.name}</h3>

              <div className="product-info">
                <span className="product-detail">SKU: {item.sku}</span>
                <span className="product-detail">
                  Quantity: {item.quantity}
                </span>
                <span className="product-detail">
                  Reorder Level: {item.reorder_level}
                </span>
                <span className="product-detail">Brand: {item.brand}</span>
                <span className="product-category">
                  Category: {item.category_id}
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* ---------- CATEGORY CARDS ---------- */
        <div className="category-list">
          {items.map((item: any) => (
            <div className="product-card" key={item.id}>
              <h3 className="product-title">{item.title}</h3>

              <div className="product-info">
                <span className="product-detail">
                  Description: {item.description}
                </span>
                <span className="product-category">Category ID: {item.id}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ProductDashboard;
