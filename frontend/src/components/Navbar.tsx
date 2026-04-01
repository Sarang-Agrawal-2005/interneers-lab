import React from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";

interface NavbarProps {
  onSelect: (value: "products" | "categories") => void;
}

function Navbar({ onSelect }: NavbarProps) {
  return (
    <nav className="navbar">
      {/* FIRST ROW: logo + dashboard/crud */}
      <div className="navbar-top">
        <div className="navbar-logo">Inventory Management System</div>

        <div className="navbar-center">
          <Link to="/dashboard">
            <button>Dashboard</button>
          </Link>

          <Link to="/crud">
            <button>CRUD</button>
          </Link>
        </div>
      </div>

      {/* SECOND ROW: products/categories */}
      <div className="navbar-bottom">
        <button onClick={() => onSelect("products")}>Products</button>
        <button onClick={() => onSelect("categories")}>Categories</button>
      </div>
    </nav>
  );
}

export default Navbar;
