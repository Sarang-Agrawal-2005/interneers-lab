# domain entities
from Products.domain.product_response import ProductResponse

class ProductEntity: # represents a product, used by the repository layer to convert ORM models to domain entities and vice versa
    def __init__(self, sku, name, quantity, reorder_level, created_at, updated_at, category_id, brand):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.created_at = created_at
        self.updated_at = updated_at
        self.category_id = category_id
        self.brand = brand



    