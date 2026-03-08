class ProductCategoryResponse(): # API response model, used by service layer to give outputs to api layer

    def __init__(self, id, title, description, created_at, updated_at):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self): # used by api layer to convert the response model to a dictionary that can be returned as a JSON response
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "created_at" : self.created_at,
            "updated_at" : self.updated_at,
        }