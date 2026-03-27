import react from "react";

function ProductItem(props: { item: String }) {
  return <li>{props.item}</li>;
}

function ProductList(props: { products: String[] }) {
  return (
    <ul>
      {props.products.map((item) => {
        return <ProductItem item={item} />;
      })}
    </ul>
  );
}

export default ProductList;
