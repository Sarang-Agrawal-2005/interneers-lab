class CreateProductRequest:  # API request models, used by api layer to give inputs to service layer
    def __init__(self, sku, name, quantity, reorder_level, created_at, updated_at, category_id):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.created_at = created_at
        self.updated_at = updated_at
        self.category_id = category_id

class UpdateProductRequest: 
    def __init__(self, name, quantity, reorder_level, updated_at, category_id):
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.updated_at = updated_at
        self.category_id = category_id