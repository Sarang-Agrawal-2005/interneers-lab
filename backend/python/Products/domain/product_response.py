class ProductResponse(): # API response model, used by service layer to give outputs to api layer

    def __init__(self, sku, name, quantity, reorder_level):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level

    def to_dict(self): # used by api layer to convert the response model to a dictionary that can be returned as a JSON response
        return {
            "sku" : self.sku,
            "name" : self.name,
            "quantity" : self.quantity,
            "reorder_level" : self.reorder_level
        }