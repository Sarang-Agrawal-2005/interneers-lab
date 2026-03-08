from Products.domain.product_category import ProductCategoryEntity
from Products.repository.product_model import ProductModel
from Products.repository.product_category_model import ProductCategoryModel

# called by the service layer to perform the actual crud operations
# handles actual crud operations and conversion logic between django/mongodb models and domain entties

class ProductCategoryRepository():

    def get_all(self):
        orm_categories = ProductCategoryModel.objects()
        return [self.convert(c) for c in orm_categories]
    
    def get_category_by_id(self, category_id):
        orm_category = ProductCategoryModel.objects(id = category_id).first()

        if not orm_category:
            return None
        
        return self.convert(orm_category)
        

    
    def create_product_category(self, payload: ProductCategoryEntity):

        title_exists = ProductCategoryModel.objects(title = payload.title).first()

        if title_exists:
            return None

        orm_category = ProductCategoryModel(
            title = payload.title,
            description = payload.description,
            created_at = payload.created_at,
            updated_at = payload.updated_at

        )

        orm_category.save()

        return self.convert(orm_category)
    
    def update_product_category(self, category_id, update_payload: ProductCategoryEntity):
        
        orm_category = ProductCategoryModel.objects(id = category_id).first()

        if not orm_category:
            return None

        if update_payload.title:
            orm_category.title = update_payload.title
        if update_payload.description:
            orm_category.description = update_payload.description
        
        
        orm_category.updated_at = update_payload.updated_at

        orm_category.save()

        return self.convert(orm_category)
        
    
    def delete_product_category(self, category_id):
        
        orm_category = ProductCategoryModel.objects(id = category_id).first()

        if not orm_category:
            return False

        orm_category.delete()
        return True
        
        
    
    def convert(self, orm_obj): # INTERNAL CONVERTER (ORM TO DOMAIN ENTITY)
        return ProductCategoryEntity(
            id=str(orm_obj.id),
            title=orm_obj.title,
            description=orm_obj.description,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at
        )



