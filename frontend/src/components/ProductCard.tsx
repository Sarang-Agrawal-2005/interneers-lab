import { Link } from "react-router-dom";

function ProductCard({
  item,
  isOpen,
  toggleExpand,
}: {
  item: any;
  isOpen: boolean;
  toggleExpand: (id: string | number) => void;
}) {
  return (
    <div
      className={`product-card ${isOpen ? "open" : ""}`}
      onClick={() => toggleExpand(item.sku)}
    >
      <h3 className="product-title">{item.name}</h3>

      {isOpen && (
        <div>
          <div className="product-info">
            <span className="product-detail">SKU: {item.sku}</span>
            <span className="product-detail">Quantity: {item.quantity}</span>
            <span className="product-detail">
              Reorder Level: {item.reorder_level}
            </span>
            <span className="product-detail">Brand: {item.brand}</span>
            <span className="product-category">
              Category: {item.category_id}
            </span>
          </div>

          <Link to={`/products/${item.sku}`}>
            <button>View Details</button>{" "}
          </Link>
        </div>
      )}
    </div>
  );
}

export default ProductCard;
