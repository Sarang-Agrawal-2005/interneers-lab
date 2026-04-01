import React, { useEffect, useState } from "react";
import "./ProductDashboard.css";
import ProductCard from "./ProductCard";
import CategoryCard from "./CategoryCard";

function ProductDashboard({ page }: { page: "products" | "categories" }) {
  const [items, setItems] = useState([]);
  const [expandedId, setExpandedId] = useState<string | number | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/${page}/`)
      .then((res) => res.json())
      .then((data) => setItems(data))
      .catch((err) => console.error(err));

    setExpandedId(null); // reset expanded card when switching tabs
  }, [page]);

  const toggleExpand = (id: string | number) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="main-container">
      <div className="product-dashboard">
        {items.length === 0 ? (
          <p className="loading-text">Loading {page}...</p>
        ) : page === "products" ? (
          <div className="product-grid">
            {items.map((item: any) => (
              <ProductCard
                key={item.sku}
                item={item}
                isOpen={expandedId === item.sku}
                toggleExpand={toggleExpand}
              />
            ))}
          </div>
        ) : (
          <div className="product-grid">
            {items.map((item: any) => (
              <CategoryCard
                key={item.id}
                item={item}
                isOpen={expandedId === item.id}
                toggleExpand={toggleExpand}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProductDashboard;
