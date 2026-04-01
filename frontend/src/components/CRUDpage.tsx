import React from "react";
import CreateProductForm from "./CraeteProductForm";
import CreateCategoryForm from "./CreateCategoryFom";
import ReadItemForm from "./ReadItemForm";
import UpdateProductForm from "./UpdateProductForm";
import UpdateCategoryForm from "./UpdateCategoryForm";
import DeleteItemForm from "./DeleteItemForm";
import "./CRUDpage.css";
function CRUDpage({
  selectedPage,
}: {
  selectedPage: "products" | "categories";
}) {
  return (
    <>
      <div className="main-container">
        <div className="CRUD-container">
          {/* CREATE */}
          <section className="section">
            <h2>
              Create{" "}
              {selectedPage.charAt(0).toUpperCase() + selectedPage.slice(1)}
            </h2>
            {selectedPage === "products" ? (
              <CreateProductForm />
            ) : (
              <CreateCategoryForm />
            )}
          </section>

          {/* UPDATE */}
          <section className="section">
            <h2>
              Update{" "}
              {selectedPage.charAt(0).toUpperCase() + selectedPage.slice(1)}
            </h2>
            {selectedPage === "products" ? (
              <UpdateProductForm />
            ) : (
              <UpdateCategoryForm />
            )}
          </section>
        </div>
        <div className="CRUD-container">
          {/* READ */}
          <section className="section">
            <h2>
              Read{" "}
              {selectedPage.charAt(0).toUpperCase() + selectedPage.slice(1)}
            </h2>
            <ReadItemForm type={selectedPage} />
          </section>

          {/* DELETE */}
          <section className="section">
            <h2>
              Delete{" "}
              {selectedPage.charAt(0).toUpperCase() + selectedPage.slice(1)}
            </h2>
            <DeleteItemForm type={selectedPage} />
          </section>
        </div>
      </div>
    </>
  );
}

export default CRUDpage;
