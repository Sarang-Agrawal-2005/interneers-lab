from Products.domain.product import ProductEntity
from Products.domain.product_request import CreateProductRequest, UpdateProductRequest
from Products.domain.product_response import ProductResponse

# api layer calls the service layer
# service layer executes the business logic
# but it does not handle actual database crud operations, it offloads those tasks to the repository layer

def entity_to_response(product: ProductEntity): # function to convert the product entity to a product response model
        return ProductResponse(
            sku = product.sku,
            name = product.name,
            quantity = product.quantity,
            reorder_level = product.reorder_level,
            created_at = product.created_at,
            updated_at = product.updated_at,
            category_id = product.category_id
        )

class ProductServices():
    def __init__(self, repository):
        self.repo = repository
    
    def list_products(self):
        products = self.repo.get_all()

        return [entity_to_response(p) for p in products]
    
    def get_product(self, sku):
        if not sku:
            raise ValueError("sku is required")
        
        product = self.repo.get_by_sku(sku)

        if not product:
            return None

        return entity_to_response(product)
    
    def create_product(self, payload: CreateProductRequest):

        if self.get_product(payload.sku) is not None:
            raise ValueError("sku is not unique")
        

        create = ProductEntity(
            sku = payload.sku,
            name = payload.name,
            quantity = payload.quantity,
            reorder_level = payload.reorder_level,
            created_at = payload.created_at,
            updated_at = payload.updated_at,
            category_id = payload.category_id
        )
        
        product = self.repo.create_product(create)

        if not product:
            raise ValueError("sku is not unique")

        return entity_to_response(product)
    
    def update_product(self, sku, payload: UpdateProductRequest):

        update = ProductEntity(
            sku = sku, # wont be chnaged by repo layer
            name = payload.name,
            quantity = payload.quantity,
            reorder_level = payload.reorder_level,
            created_at = None, # wont be chnaged by repo layer
            updated_at = payload.updated_at,
            category_id = payload.category_id
        )
        
        product = self.repo.update_product(sku, update)

        if not product:
            return None

        return entity_to_response(product)
    
    def delete_product(self, sku):
        if not sku:
            raise ValueError("sku is required")
        
        return self.repo.delete_product(sku)
    
    def list_products_of_category(self, category_id):
        if not category_id:
            raise ValueError("Category is required")
        
        products = self.repo.get_products_of_category(category_id)

        if products is None:
            return None

        return [entity_to_response(p) for p in products]
    
    def assign_category(self, sku, category_id):
        if not category_id:
            raise ValueError("Category is required")
        
        product = self.repo.add_category(sku, category_id)

        if product is None:
            return None

        return entity_to_response(product)
    
    def remove_category(self, sku, category_id):
        if not category_id:
            raise ValueError("Category is required")
        if not sku:
            raise ValueError("sku is required")
        
        product = self.repo.remove_category(sku, category_id)

        if product is None:
            return None

        return entity_to_response(product)

    