# domain entities
from Products.domain.product_response import ProductResponse

class ProductEntity: # represents a product, used by the repository layer to convert ORM models to domain entities and vice versa
    def __init__(self, sku, name, quantity, reorder_level):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level

    