from Products.domain.product import ProductEntity

# api layer calls the service layer
# service layer executes the business logic
# but it does not handle actual database crud operations, it offloads those tasks to the repository layer

class ProductServices():
    def __init__(self, repository):
        self.repo = repository
    
    def list_products(self):
        return self.repo.get_all()
    
    def get_product(self, sku):
        if not sku:
            raise ValueError("sku is required")
        
        product = self.repo.get_by_sku(sku)
        return product
    
    def create_product(self, sku, name, quantity, reorder_level):
        if not sku or not name:
            raise ValueError("sku and name required")
        if quantity < 0:
            raise ValueError("quantity cannot be less than zero")
        if reorder_level < 0:
            raise ValueError("reorder value cannot be less than zero")
        
        product = ProductEntity(
            sku = sku,
            name = name,
            quantity = quantity,
            reorder_level = reorder_level
        )

        return self.repo.create_product(product)
    
    def update_product(self, sku, name, quantity, reorder_level):
        if quantity < 0:
            raise ValueError("quantity cannot be less than zero")
        if reorder_level < 0:
            raise ValueError("reorder value cannot be less than zero")
        
        product = ProductEntity(
            sku = sku,
            name = name,
            quantity = quantity,
            reorder_level = reorder_level
        )

        return self.repo.update_product(sku, product)
    
    def delete_product(self, sku):
        if not sku:
            raise ValueError("sku is required")
        
        return self.repo.delete_product(sku)
    