import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import CreateProductForm from "./components/CraeteProductForm";
import CreateCategoryForm from "./components/CreateCategoryFom";
import ReadItemForm from "./components/ReadItemForm";
import UpdateProductForm from "./components/UpdateProductForm";
import UpdateCategoryForm from "./components/UpdateCategoryForm";
import DeleteItemForm from "./components/DeleteItemForm";
import "./App.css";

function App() {
  // tracks selected menu
  const [selectedPage, setSelectedPage] = useState<"products" | "categories">(
    "products",
  );

  // // data from API
  // const [items, setItems] = useState([]);

  // // fetch real data whenever selectedPage changes
  // useEffect(() => {
  //   fetch(`http://localhost:8000/api/${selectedPage}/`)
  //     .then((res) => res.json())
  //     .then((data) => setItems(data))
  //     .catch((err) => console.error(err));
  // }, [selectedPage]);

  return (
    <div>
      <Navbar onSelect={setSelectedPage} />

      <div className="main-container">
        {/* CREATE */}
        <section className="section">
          <h2>Create</h2>
          {selectedPage === "products" ? (
            <CreateProductForm />
          ) : (
            <CreateCategoryForm />
          )}
        </section>

        {/* READ */}
        <section className="section">
          <h2>Read</h2>
          <ReadItemForm type={selectedPage} />
        </section>

        {/* UPDATE */}
        <section className="section">
          <h2>Update</h2>
          {selectedPage === "products" ? (
            <UpdateProductForm />
          ) : (
            <UpdateCategoryForm />
          )}
        </section>

        {/* DELETE */}
        <section className="section">
          <h2>Delete</h2>
          <DeleteItemForm type={selectedPage} />
        </section>
      </div>

      <Footer />
    </div>
  );
}

export default App;
