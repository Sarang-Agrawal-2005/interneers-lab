class CreateProductRequest:  # API request models, used by api layer to give inputs to service layer
    def __init__(self, sku, name, quantity, reorder_level):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level

class UpdateProductRequest: 
    def __init__(self, name, quantity, reorder_level):
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level