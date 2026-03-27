import React from "react";
import "./Navbar.css";

interface NavbarProps {
  onSelect: (value: "products" | "categories") => void;
}

function Navbar({ onSelect }: NavbarProps) {
  return (
    <nav className="navbar">
      <div className="navbar-logo">Inventory Management System</div>

      <ul className="navbar-links">
        <li onClick={() => onSelect("products")}>Products</li>
        <li onClick={() => onSelect("categories")}>Categories</li>
      </ul>
    </nav>
  );
}

export default Navbar;
