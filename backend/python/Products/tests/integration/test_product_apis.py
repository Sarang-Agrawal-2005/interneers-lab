from django.test import TestCase, Client
from mongoengine import connect, disconnect
from datetime import datetime, timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from Products.repository.product_model import ProductModel
from Products.repository.product_category_model import ProductCategoryModel


class ProductIntegrationTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Ensure test DB is used
        disconnect()
        connect(
            db="inventory_test",
            host="mongodb://root:example@localhost:27019/inventory_test?authSource=admin"
        )

        cls.client = Client()

        ProductCategoryModel.objects.delete()

        # Seed one category for use in tests
        cls.category = ProductCategoryModel(
            title="Test Category",
            description="Testing category",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        cls.category.save()  # save first

        cls.category = ProductCategoryModel.objects.first()

    def tearDown(self):
        """Clear DB after each test"""
        ProductModel.objects.delete()

    # -------------------------------------------------------------------------
    # LIST PRODUCTS
    # -------------------------------------------------------------------------
    def test_list_products(self):

        # Adding 2 products to database
        
        p1 = ProductModel(
            sku=100, name="Item A", quantity=10, reorder_level=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            category=self.category, brand="BrandA"
        ).save()

        p2 = ProductModel(
            sku=101, name="Item B", quantity=20, reorder_level=5,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            category=self.category, brand="BrandB"
        ).save()

        result = self.client.get("/api/products/") # should return the 2 products saved
        data = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(data), 2)

    # -------------------------------------------------------------------------
    # GET PRODUCT BY SKU
    # -------------------------------------------------------------------------
    def test_get_product(self):

        # adding a product to db

        p = ProductModel(
            sku=250, name="Item", quantity=10, reorder_level=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            category=self.category, brand="Brand"
        ).save()

        result = self.client.get(f"/api/products/250/") # should return the saved proudct

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["sku"], 250)

    def test_get_product_not_found(self):
        res = self.client.get("/api/products/999999/")
        self.assertEqual(res.status_code, 404)

    # -------------------------------------------------------------------------
    # CREATE PRODUCT
    # -------------------------------------------------------------------------
    def test_create_product(self):

        payload = {   # data sent by client to create product
            "sku": 300,
            "name": "Created Product",
            "quantity": 50,
            "reorder_level": 10,
            "category_id": str(self.category.id),
            "brand": "CreateBrand"
        }

        result = self.client.post("/api/products/create", payload, content_type="application/json")

        self.assertEqual(result.status_code, 201)
        product = ProductModel.objects(sku=300).first()
        self.assertIsNotNone(product)

    def test_create_product_invalid(self):
        payload = {  # missing required "sku"
            "name": "Invalid",
            "quantity": 5,
            "reorder_level": 1,
            "category_id": str(self.category.id),
            "brand": "X"
        }

        res = self.client.post("/api/products/create", payload, content_type="application/json") # should return bad request as data wont pass serializer

        self.assertEqual(res.status_code, 400)

    def test_create_product_sku_not_unique(self):
        
        product = ProductModel(
            sku=2000, name="GetTest", quantity=30, reorder_level=3,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            category=self.category, brand="BrandX"
        ).save()

        payload = {
            "sku": 2000,  
            "name": "Invalid",
            "quantity": 5,
            "reorder_level": 1,
            "category_id": str(self.category.id),
            "brand": "X"
        }

        res = self.client.post("/api/products/create", payload, content_type="application/json") # should return bad request

        self.assertEqual(res.status_code, 400)

    # -------------------------------------------------------------------------
    # UPDATE PRODUCT
    # -------------------------------------------------------------------------
    def test_update_product(self):

        product = ProductModel(
            sku=400, name="Before Update", quantity=10, reorder_level=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            category=self.category, brand="OldBrand"
        ).save()

        payload = {
            "name": "After Update",
            "quantity": 99,
            "reorder_level": 9,
            "category_id": str(self.category.id),
            "brand": "NewBrand"
        }

        result = self.client.put(
            f"/api/products/update/{product.sku}/",
            payload,
            content_type="application/json"
        )

        self.assertEqual(result.status_code, 200)
        updated = ProductModel.objects(sku=400).first()
        self.assertEqual(updated.name, "After Update")
        self.assertEqual(updated.brand, "NewBrand")

    def test_update_product_not_found(self):
        payload = {
            "name": "Update",
            "quantity": 10,
            "reorder_level": 1,
            "category_id": str(self.category.id),
            "brand": "Brand"
        }

        result = self.client.put("/api/products/update/99999/", payload, content_type="application/json")
        self.assertEqual(result.status_code, 404)

    # -------------------------------------------------------------------------
    # DELETE PRODUCT
    # -------------------------------------------------------------------------
    def test_delete_product(self):

        product = ProductModel(
            sku=500, name="DeleteMe", quantity=5, reorder_level=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            category=self.category, brand="DelBrand"
        ).save()

        result = self.client.delete(f"/api/products/delete/{product.sku}/")

        self.assertEqual(result.status_code, 204)
        self.assertIsNone(ProductModel.objects(sku=500).first())

    def test_delete_product_not_found(self):
        result = self.client.delete("/api/products/delete/99999/")
        self.assertEqual(result.status_code, 404)

    # -------------------------------------------------------------------------
    # BULK CSV UPLOAD
    # -------------------------------------------------------------------------
    def test_bulk_create_products(self):

        csv_content = (
            "sku,name,quantity,reorder_level,category_id,brand\n"
            f"601,BulkItem1,10,2,{self.category.id},Brand1\n"
            f"602,BulkItem2,20,3,{self.category.id},Brand2\n"
        ).encode("utf-8")

        csv_file = SimpleUploadedFile("bulk.csv", csv_content, content_type="text/csv")

        res = self.client.post("/api/products/create/bulk", {"file": csv_file})

        self.assertEqual(res.status_code, 201)
        self.assertEqual(ProductModel.objects.count(), 2)

    def test_bulk_create_invalid_row(self):

        csv_content = (
            "sku,name,quantity,reorder_level,category_id,brand\n"
            f"700,BulkItem,abc,3,{self.category.id},BrandX\n"   # invalid: quantity=abc
        ).encode("utf-8")

        csv_file = SimpleUploadedFile("bad.csv", csv_content, content_type="text/csv")

        res = self.client.post("/api/products/create/bulk", {"file": csv_file})
        self.assertEqual(res.status_code, 400)