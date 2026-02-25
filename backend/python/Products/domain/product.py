# domain entities

class ProductEntity: # Python class that represents a product
    def __init__(self, sku, name, quantity, reorder_level):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level