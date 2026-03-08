from Products.domain.product import ProductEntity
from Products.repository.product_model import ProductModel
from Products.repository.product_category_model import ProductCategoryModel

# called by the service layer to perform the actual crud operations
# handles actual crud operations and conversion logic between django/mongodb models and domain entties

class ProductRepository():

    def get_all(self):
        orm_products = ProductModel.objects()
        return [self.convert(p) for p in orm_products]
    
    def get_by_sku(self, sku):
        orm_product = ProductModel.objects(sku = sku).first()

        if not orm_product:
            return None
        return self.convert(orm_product)
        

    
    def create_product(self, payload: ProductEntity):

        category = None

        if payload.category_id:
            category = ProductCategoryModel.objects(id = payload.category_id).first()

            if not category:
                raise ValueError("Category does not exist")

        
        orm_product = ProductModel(
            sku = payload.sku,
            name = payload.name,
            quantity = payload.quantity,
            reorder_level = payload.reorder_level,
            created_at = payload.created_at,
            updated_at = payload.updated_at,
            category = category

        )

        orm_product.save()

        return self.convert(orm_product)
    
    def update_product(self, sku, update_payload: ProductEntity):
        
        orm_product = ProductModel.objects(sku = sku).first()

        if not orm_product:
            return None

        if update_payload.name is not None:
            orm_product.name = update_payload.name
        if update_payload.quantity is not None:
            orm_product.quantity = update_payload.quantity
        if update_payload.reorder_level is not None:
            orm_product.reorder_level = update_payload.reorder_level
        

        if update_payload.category_id is not None:
            category = ProductCategoryModel.objects(id = update_payload.category_id).first()

            if not category:
                raise ValueError("Category does not exist")
            else:
                orm_product.category = category
        
        orm_product.updated_at = update_payload.updated_at

        orm_product.save()

        return self.convert(orm_product)
        
    
    def delete_product(self, sku):
        
        orm_product = ProductModel.objects(sku = sku).first()

        if not orm_product:
            return False

        orm_product.delete()
        return True
        
        
    
    def convert(self, orm_obj): # INTERNAL CONVERTER (ORM -> DOMAIN)
        return ProductEntity(
            sku=orm_obj.sku,
            name=orm_obj.name,
            quantity=orm_obj.quantity,
            reorder_level=orm_obj.reorder_level,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
            category_id=str(orm_obj.category.id) if orm_obj.category else None
        )



