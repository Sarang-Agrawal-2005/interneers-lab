import unittest
from unittest.mock import MagicMock
from datetime import datetime

from Products.service.product_category_service import ProductCategoryServices
from Products.domain.product_category import ProductCategoryEntity
from Products.domain.product_category_request import CreateProductCategoryRequest, UpdateProductCategoryRequest
from Products.domain.product_category_response import ProductCategoryResponse


class TestProductCategoryService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = ProductCategoryServices(self.mock_repo)

    # --------------------------------------------------------------------
    # LIST
    # --------------------------------------------------------------------
    def test_list_product_categories(self):
        cat1 = ProductCategoryEntity("1", "Electronics", "desc", datetime.now(), datetime.now())
        cat2 = ProductCategoryEntity("2", "Fashion", "desc2", datetime.now(), datetime.now())

        self.mock_repo.get_all.return_value = [cat1, cat2]

        result = self.service.list_product_categories()

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], ProductCategoryResponse)
        self.assertEqual(result[0].title, "Electronics")
        self.assertIsInstance(result[1], ProductCategoryResponse)
        self.assertEqual(result[1].title, "Fashion")

        self.mock_repo.get_all.assert_called_once()

    def test_list_product_categories_empty_result(self):

        self.mock_repo.get_all.return_value = []

        result = self.service.list_product_categories()

        self.assertEqual(result, [])   # Should be empty list
        self.mock_repo.get_all.assert_called_once_with()

    # --------------------------------------------------------------------
    # GET BY ID
    # --------------------------------------------------------------------
    def test_get_product_category_success(self):
        cat = ProductCategoryEntity("1", "Groceries", "desc", datetime.now(), datetime.now())
        self.mock_repo.get_category_by_id.return_value = cat

        result = self.service.get_product_category("1")

        self.assertIsInstance(result, ProductCategoryResponse)
        self.assertEqual(result.id, "1")

        self.mock_repo.get_category_by_id.assert_called_once_with("1")

    def test_get_product_category_not_found(self):
        self.mock_repo.get_category_by_id.return_value = None

        result = self.service.get_product_category("999")
        self.assertIsNone(result)

    def test_get_product_category_missing_id(self):
        with self.assertRaises(ValueError) as context:
            self.service.get_product_category(None)

        self.assertEqual(str(context.exception), "category is required")

    # # --------------------------------------------------------------------
    # # CREATE
    # # --------------------------------------------------------------------
    def test_create_product_category_success(self):
        payload = CreateProductCategoryRequest(
            title="Sports",
            description="All sports items",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        saved_entity = ProductCategoryEntity("10", payload.title, payload.description, payload.created_at, payload.updated_at)

        self.mock_repo.create_product_category.return_value = saved_entity

        result = self.service.create_product_category(payload)

        self.assertIsInstance(result, ProductCategoryResponse)
        self.assertEqual(result.title, "Sports")
        self.assertEqual(result.id, "10")

        self.mock_repo.create_product_category.assert_called_once()

    def test_create_product_category_title_not_unique(self):
        payload = CreateProductCategoryRequest("Books", "desc", datetime.now(), datetime.now())

        self.mock_repo.create_product_category.return_value = None

        with self.assertRaises(ValueError) as context:
            self.service.create_product_category(payload)

        self.assertEqual(str(context.exception), "title is not unique")

    # # --------------------------------------------------------------------
    # # UPDATE
    # # --------------------------------------------------------------------
    def test_update_product_category_success(self):
        existing = ProductCategoryEntity("5", "Old", "Old desc", datetime.now(), datetime.now())
        self.mock_repo.get_category_by_id.return_value = existing

        payload = UpdateProductCategoryRequest("New Title", "New Desc", datetime.now())

        updated_entity = ProductCategoryEntity("5", payload.title, payload.description, existing.created_at, payload.updated_at)
        self.mock_repo.update_product_category.return_value = updated_entity

        result = self.service.update_product_category("5", payload)

        self.assertIsInstance(result, ProductCategoryResponse)
        self.assertEqual(result.title, "New Title")

        self.mock_repo.get_category_by_id.assert_called_once_with("5")
        self.mock_repo.update_product_category.assert_called_once()

    def test_update_product_category_not_found(self):
        self.mock_repo.get_category_by_id.return_value = None

        payload = UpdateProductCategoryRequest("X", "Y", datetime.now())
        result = self.service.update_product_category("999", payload)

        self.assertIsNone(result)

    def test_update_product_category_missing_id(self):
        payload = UpdateProductCategoryRequest("X", "Y", datetime.now())

        with self.assertRaises(ValueError) as context:
            self.service.update_product_category(None, payload)

        self.assertEqual(str(context.exception), "category is required")

    # # --------------------------------------------------------------------
    # # DELETE
    # # --------------------------------------------------------------------
    def test_delete_product_category_success(self):
        self.mock_repo.delete_product_category.return_value = True

        result = self.service.delete_product_category("1")
        self.assertTrue(result)

        self.mock_repo.delete_product_category.assert_called_once_with("1")

    def test_delete_product_category_not_found(self):
        self.mock_repo.delete_product_category.return_value = False

        result = self.service.delete_product_category("999")
        self.assertFalse(result)

    def test_delete_product_category_missing_id(self):
        with self.assertRaises(ValueError) as context:
            self.service.delete_product_category(None)
        
        self.assertEqual(str(context.exception), "category is required")


if __name__ == "__main__":
    unittest.main()