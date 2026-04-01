import { Link } from "react-router-dom";

function CategoryCard({
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
      onClick={() => toggleExpand(item.id)}
    >
      <h3 className="product-title">{item.title}</h3>

      {isOpen && (
        <div>
          <div className="product-info">
            <span className="product-detail">
              Description: {item.description}
            </span>
            <span className="product-category">Category ID: {item.id}</span>
          </div>

          <Link to={`/categories/${item.id}`}>
            <button>View Details</button>{" "}
          </Link>
        </div>
      )}
    </div>
  );
}

export default CategoryCard;
