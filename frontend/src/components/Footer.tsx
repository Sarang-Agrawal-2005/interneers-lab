import React from "react";
import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>Inventory App</h3>
          <p>Built for learning React + TypeScript.</p>
        </div>

        <div className="footer-section">
          <h4>Links</h4>
          <ul>
            <li>
              <a href="#">Products</a>
            </li>
            <li>
              <a href="#">Categories</a>
            </li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Contact</h4>
          <p>Email: support@example.com</p>
        </div>
      </div>

      <div className="footer-bottom">
        © {new Date().getFullYear()} Inventory System. All rights reserved.
      </div>
    </footer>
  );
}

export default Footer;
