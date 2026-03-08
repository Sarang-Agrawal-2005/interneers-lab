class CreateProductCategoryRequest:  # API request models, used by api layer to give inputs to service layer
    def __init__(self, title, description, created_at, updated_at):
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        

class UpdateProductCategoryRequest: 
    def __init__(self, title, description, updated_at):
        self.title = title
        self.description = description
        self.updated_at = updated_at
        