async function loadProducts(filters = {}) {
    let query = new URLSearchParams();

    if (filters.brand) query.append("brand", filters.brand);
    if (filters.min_qty) query.append("min_qty", filters.min_qty);
    if (filters.max_qty) query.append("max_qty", filters.max_qty);

    if (filters.sort_by) query.append("sort_by", filters.sort_by);
    if (filters.order) query.append("order", filters.order);

    if (filters.page){
        query.append("page", filters.page);
    }
    else{
        query.append("page", 1);
    }

    if (filters.page_size){
        query.append("page_size", filters.page_size);
    }
    else{
        query.append("page_size", 12);
    }

    const res = await fetch(`http://127.0.0.1:8000/api/products/?${query.toString()}`);
    const products = await res.json();

    const container = document.getElementById("product-container");
    if (!container) return; // prevent errors on categories page
    container.innerHTML = "";

    products.forEach(p => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
            <h3>${p.name}</h3>
            <p><strong>SKU:</strong> ${p.sku}</p>
            <p><strong>Brand:</strong> ${p.brand}</p>
            <p><strong>Quantity:</strong> ${p.quantity}</p>
            <p><strong>Reorder Level:</strong> ${p.reorder_level}</p>
            <p><strong>Created At:</strong> ${p.created_at}</p>
            <p><strong>Updated At:</strong> ${p.updated_at}</p>
        `;
        container.appendChild(card);
    });
}

async function loadCategories() {
    const res = await fetch("http://127.0.0.1:8000/api/categories/");
    const categories = await res.json();

    const container = document.getElementById("category-container");
    if (!container) return; // prevent errors on products page
    container.innerHTML = "";

    categories.forEach(c => {
        const card = document.createElement("div");
        card.className = "category-card";
        card.innerHTML = `
            <h3>${c.title}</h3>
            <p><strong>Id:</strong> ${c.id}</p>
            <p><strong>Description:</strong> ${c.description}</p>
            <p><strong>Created At:</strong> ${c.created_at}</p>
            <p><strong>Updated At:</strong> ${c.updated_at}</p>
        `;
        container.appendChild(card);
    });
}

// FILTER BUTTON
const applyFiltersBtn = document.getElementById("apply-filters");
if (applyFiltersBtn) {
    applyFiltersBtn.addEventListener("click", () => {
        const filters = {
            brand: document.getElementById("filter-brand").value,
            min_qty: document.getElementById("filter-min-qty").value,
            max_qty: document.getElementById("filter-max-qty").value,
            sort_by: document.getElementById("filter-sort-by").value,
            order: document.getElementById("filter-order").value,
            page: document.getElementById("filter-page-no").value,
            page_size: document.getElementById("filter-page-size").value,
        };
        loadProducts(filters);
    });
}

// PRODUCTS PAGE
const productReloadBtn = document.getElementById("reload-btn");
if (productReloadBtn) {
    productReloadBtn.addEventListener("click", loadProducts);
    loadProducts();
}

// CATEGORIES PAGE
const categoryReloadBtn = document.getElementById("reload-category-btn");
if (categoryReloadBtn) {
    categoryReloadBtn.addEventListener("click", loadCategories);
    loadCategories();
}