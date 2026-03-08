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
            updated_at = product.updated_at
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
            updated_at = payload.updated_at
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
            updated_at = payload.updated_at
        )
        
        product = self.repo.update_product(sku, update)

        if not product:
            return None

        return entity_to_response(product)
    
    def delete_product(self, sku):
        if not sku:
            raise ValueError("sku is required")
        
        return self.repo.delete_product(sku)
    