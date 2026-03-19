import json
from django.test import TestCase, Client
from mongoengine import connect, disconnect
from datetime import datetime, timezone
from bson import ObjectId

from Products.repository.product_category_model import ProductCategoryModel
from Products.repository.product_model import ProductModel


class CategoryIntegrationTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        disconnect()
        connect(
            db="inventory_test",
            host="mongodb://root:example@localhost:27019/inventory_test?authSource=admin"
        )

        cls.client = Client()

    def setUp(self):
        ProductCategoryModel.objects.delete()
        ProductModel.objects.delete()

        now = datetime.now(timezone.utc)

        # Create a test category
        self.category = ProductCategoryModel(
            title="Test Category",
            description="Description",
            created_at=now,
            updated_at=now,
        ).save()

        # Create another category
        self.other_category = ProductCategoryModel(
            title="Other Category",
            description="Another Desc",
            created_at=now,
            updated_at=now,
        ).save()

        # Create a product under category
        self.product = ProductModel(
            sku=100,
            name="Sample Product",
            quantity=50,
            reorder_level=10,
            created_at=now,
            updated_at=now,
            category=self.category,
            brand="BrandX"
        ).save()

    # -----------------------------
    # GET /categories/
    # -----------------------------
    def test_list_categories(self):
        res = self.client.get("/api/categories/")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.json()), 2) # should return the 2 saved categories during setup phase

    # -----------------------------
    # GET /categories/<id>
    # -----------------------------
    def test_get_category(self):
        url = f"/api/categories/{str(self.category.id)}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["title"], "Test Category")

    def test_get_category_invalid_id(self):
        res = self.client.get("/api/categories/INVALID_ID")
        self.assertEqual(res.status_code, 400)

    def test_get_category_not_found(self):
        fake_id = str(ObjectId())
        res = self.client.get(f"/categories/{fake_id}")
        self.assertEqual(res.status_code, 404)

    # -----------------------------
    # POST /categories/create/
    # -----------------------------
    def test_create_category(self):

        payload = {  # data sent by client
            "title": "New Category",
            "description": "Created via test"
        }

        res = self.client.post("/api/categories/create/", payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["title"], "New Category")

    def test_create_category_invalid_payload(self):
        res = self.client.post("/api/categories/create/", {"title": ""})
        self.assertEqual(res.status_code, 400)

    # -----------------------------
    # PUT /categories/update/<id>/
    # -----------------------------
    def test_update_category(self):
        url = f"/api/categories/update/{str(self.category.id)}/"
        payload = {
            "title": "Updated Title",
            "description": "Updated Desc"
        }
        res = self.client.put(url, data=json.dumps(payload), content_type="application/json")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["title"], "Updated Title")

    def test_update_category_invalid_id(self):
        res = self.client.put("/api/categories/update/INVALID_ID/", data=json.dumps({}), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_category_not_found(self):
        fake_id = str(ObjectId())
        payload = {"title": "X", "description": "Y"}

        res = self.client.put(
            f"/api/categories/update/{fake_id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 404)

    # -----------------------------
    # DELETE /categories/delete/<id>/
    # -----------------------------
    def test_delete_category(self):
        url = f"/api/categories/delete/{str(self.other_category.id)}/"
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)

    def test_delete_category_invalid_id(self):
        res = self.client.delete("/api/categories/delete/INVALID_ID/")
        self.assertEqual(res.status_code, 400)

    def test_delete_category_not_found(self):
        fake_id = str(ObjectId())
        res = self.client.delete(f"/api/categories/delete/{fake_id}/")
        self.assertEqual(res.status_code, 404)

    # -----------------------------
    # 6. GET /categories/<id>/products/
    # -----------------------------
    def test_get_products_of_category(self):
        url = f"/api/categories/{str(self.category.id)}/products/"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()[0]["sku"], 100)

    def test_get_products_of_category_invalid_id(self):
        res = self.client.get("/api/categories/INVALID_ID/products/")
        self.assertEqual(res.status_code, 400)

    # -----------------------------
    # PATCH /categories/<id>/product/add
    # -----------------------------
    def test_add_product_to_category(self):
        payload = {"sku": 100}
        url = f"/api/categories/{str(self.other_category.id)}/product/add"

        res = self.client.patch(
            url,
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["category_id"], str(self.other_category.id))

    def test_add_product_to_category_invalid_id(self):
        res = self.client.patch("/api/categories/INVALID_ID/product/add", {"sku": 100})
        self.assertEqual(res.status_code, 400)

    # -----------------------------
    # 8. PATCH /categories/<id>/product/remove/<sku>/
    # -----------------------------
    def test_remove_product_from_category(self):
        url = f"/api/categories/{str(self.category.id)}/product/remove/100/"
        res = self.client.patch(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["category_id"], None)

    def test_remove_product_from_category_invalid_id(self):
        res = self.client.patch("/api/categories/INVALID_ID/product/remove/100/")
        self.assertEqual(res.status_code, 400)