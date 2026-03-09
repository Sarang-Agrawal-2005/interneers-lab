class ProductResponse(): # API response model, used by service layer to give outputs to api layer

    def __init__(self, sku, name, quantity, reorder_level, created_at, updated_at, category_id, brand):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.created_at = created_at
        self.updated_at = updated_at
        self.category_id = category_id
        self.brand = brand

    def to_dict(self): # used by api layer to convert the response model to a dictionary that can be returned as a JSON response
        return {
            "sku" : self.sku,
            "name" : self.name,
            "quantity" : self.quantity,
            "reorder_level" : self.reorder_level,
            "created_at" : self.created_at,
            "updated_at" : self.updated_at,
            "category_id" : self.category_id,
            "brand" : self.brand
        }