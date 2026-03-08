# domain entities

class ProductCategoryEntity: # represents a product category, used by the repository layer to convert ORM models to domain entities and vice versa
    def __init__(self, id, title, description, created_at, updated_at):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        



    