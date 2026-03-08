from mongoengine import Document, StringField, IntField, DateTimeField

class ProductCategoryModel(Document):

    title = StringField(required=True, unique=True)
    description = StringField()
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    meta = {
        "collection": "product_categories"
    }