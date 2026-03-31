import React from "react";
import "./Navbar.css";

interface NavbarProps {
  onSelect: (value: "Dashboard" | "CRUD") => void;
  //onSelect is a callback function recieved from app as a prop which corresponds to the setSelectedPage function
}

function Navbar({ onSelect }: NavbarProps) {
  return (
    <nav className="navbar">
      <div className="navbar-logo">Inventory Management System</div>

      <ul className="navbar-links">
        <li onClick={() => onSelect("Dashboard")}>Dashboard</li>
        <li onClick={() => onSelect("CRUD")}>CRUD</li>
      </ul>
    </nav>
  );
}

export default Navbar;
