import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ProductDashboard from "components/ProductDashboard";
import CRUDpage from "components/CRUDpage";
import ProductPage from "components/ProductPage";
import "./App.css";

function App() {
  // tracks selected menu
  const [selectedPage, setSelectedPage] = useState<"products" | "categories">(
    "products",
  );

  return (
    <Router>
      <Navbar onSelect={setSelectedPage} />

      <div className="app-container">
        <div id="content">
          <div className="main-container">
            <Routes>
              {/* DASHBOARD PAGE */}
              <Route
                path="/dashboard"
                element={<ProductDashboard page={selectedPage} />}
              />

              {/* CRUD PAGE */}
              <Route
                path="/crud"
                element={<CRUDpage selectedPage={selectedPage} />}
              />

              <Route path="/products/:productId" element={<ProductPage />} />

              {/* DEFAULT ROUTE — redirect to products */}
              <Route path="/" element={<ProductDashboard page="products" />} />
            </Routes>
          </div>
        </div>
      </div>

      <Footer />
    </Router>
  );
}

export default App;
