import React from "react";
import "./Sidebar.css";

interface SidebarProps {
  onSelect: (value: "products" | "categories") => void;
  //onSelect is a callback function recieved from app as a prop which corresponds to the setSelectedPage function
}

function Sidebar({ onSelect }: SidebarProps) {
  return (
    <div className="Sidebar">
      <ul className="sidebar-links">
        <li onClick={() => onSelect("products")}>Products</li>
        <li onClick={() => onSelect("categories")}>Categories</li>
      </ul>
    </div>
  );
}

export default Sidebar;
