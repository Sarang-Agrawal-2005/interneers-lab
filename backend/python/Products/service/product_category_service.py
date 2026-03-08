from Products.domain.product_category import ProductCategoryEntity
from Products.domain.product_category_request import CreateProductCategoryRequest, UpdateProductCategoryRequest
from Products.domain.product_category_response import ProductCategoryResponse

# api layer calls the service layer
# service layer executes the business logic
# but it does not handle actual database crud operations, it offloads those tasks to the repository layer

def entity_to_response(category: ProductCategoryEntity): # function to convert the product entity to a product response model
        return ProductCategoryResponse(
            id = category.id,
            title = category.title,
            description = category.description,
            created_at = category.created_at,
            updated_at = category.updated_at
        )

class ProductCategoryServices():
    def __init__(self, repository):
        self.repo = repository
    
    def list_product_categories(self):
        categories = self.repo.get_all()

        return [entity_to_response(c) for c in categories]
    
    def get_product_category(self, category_id):
        if not category_id:
             raise ValueError("category is required")
        
        category = self.repo.get_category_by_id(category_id)

        if not category:
             return None

        return entity_to_response(category)
    
    def create_product_category(self, payload: CreateProductCategoryRequest):

        data = ProductCategoryEntity(
             id = None, # will be assigned by repo layer
             title = payload.title,
             description = payload.description,
             created_at = payload.created_at,
             updated_at = payload.updated_at
        )

        category = self.repo.create_product_category(data)

        if not category:
            raise ValueError("title is not unique")

        return entity_to_response(category)


    
    def update_product_category(self, category_id, payload: UpdateProductCategoryRequest):

        if not category_id:
             raise ValueError("category is required")

        category_exists = self.repo.get_category_by_id(category_id)

        if not category_exists:
            return None
        
        data = ProductCategoryEntity(
             id = None, # WONT BE CHANGED BY REPO LAYER
             title = payload.title,
             description = payload.description,
             created_at = None, # WONT BE CHANGED BY REPO LAYER
             updated_at = payload.updated_at
        )

        category = self.repo.update_product_category(category_id, data)

        return entity_to_response(category)


    
    def delete_product_category(self, category_id):
        if not category_id:
             raise ValueError("category is required")
        
        return self.repo.delete_product_category(category_id)
        