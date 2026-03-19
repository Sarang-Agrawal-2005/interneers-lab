import unittest
from unittest.mock import MagicMock

from Products.service.product_service import ProductServices
from Products.domain.product import ProductEntity
from Products.domain.product_response import ProductResponse
from Products.domain.product_request import CreateProductRequest, UpdateProductRequest
from datetime import datetime, timezone

class TestProductService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock() # Fake repository
        self.service = ProductServices(self.mock_repo) # service layer will call fake repsoitory instead of actual one

    
    # Test cases for list_products function in service layer

    def test_list_products_success(self):

        now = datetime.now(timezone.utc)

        fake_products = [ProductEntity(
            sku = 123 + i,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        ) for i in range(0,10)]

        self.mock_repo.get_all.return_value = fake_products

        filters = {}

        result = self.service.list_products(filters)

        self.assertIsNotNone(result)
        self.assertEqual([p.sku for p in fake_products], [p.sku for p in result])
        for p in result:
            self.assertIsInstance(p, ProductResponse)
        self.mock_repo.get_all.assert_called_once_with(filters)

    def test_list_products_empty_result(self):

        self.mock_repo.get_all.return_value = []

        filters = {}

        result = self.service.list_products(filters)

        self.assertEqual(result, [])   # Should be empty list
        self.mock_repo.get_all.assert_called_once_with(filters)

    def test_list_products_passes_filters_to_repo(self):
    
        filters = {
            "brand": "Nike",
            "min_qty": 10,
            "max_qty": 100,
            "sort_by": "sku",
            "order": "desc",
            "page": 5,
            "page_size": 10
        }

        self.mock_repo.get_all.return_value = []

        self.service.list_products(filters)
        self.mock_repo.get_all.assert_called_once_with(filters)

    
    # Test cases for get_product function in service layer
    
    def test_get_product_success(self):

        now = datetime.now(timezone.utc)

        fake_product = ProductEntity(
            sku = 123,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        )

        self.mock_repo.get_by_sku.return_value = fake_product # fake return value

        result = self.service.get_product(123) 

        '''the real service layers get_product function calls the get_by_sku function in the fake repo layer,
            the get_by_sku function returns the fake product, this isolate sthe service layer logic from the api and repository layer'''

        self.assertIsNotNone(result) # Ensured that the service layer returned a product
        self.assertEqual(result.sku, 123) # Ensures it is the correct product
        self.mock_repo.get_by_sku.assert_called_once_with(123) # Ensures service layer called the repo layer exactly once and with the correct argument

    def test_get_product_not_found(self):

        self.mock_repo.get_by_sku.return_value = None

        result = self.service.get_product(123)

        self.assertIsNone(result)
        self.mock_repo.get_by_sku.assert_called_once_with(123)

    def test_get_product_sku_not_found(self):

        with self.assertRaises(ValueError) as context:
            self.service.get_product(None)

        self.assertEqual(str(context.exception), "sku is required")

        # sku = empty string should also raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.get_product("")

        self.assertEqual(str(context.exception), "sku is required")


    # Test cases for create_product function in service layer

    def test_create_product_success(self):

        now = datetime.now(timezone.utc)

        fake_product = ProductEntity(
            sku = 10,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        )

        self.mock_repo.create_product.return_value = fake_product
        self.mock_repo.get_by_sku.return_value = None

        req = CreateProductRequest(
            sku = 10,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        )

        result = self.service.create_product(req)

        self.assertIsNotNone(result)
        self.assertEqual(result.sku, req.sku)
        self.assertIsInstance(result, ProductResponse)

    def test_create_product_sku_not_unique(self):

        now = datetime.now(timezone.utc)

        req = CreateProductRequest(
            sku = 10,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        )

        self.mock_repo.get_by_sku.return_value = "Not null value"

        with self.assertRaises(ValueError) as context1:
            self.service.create_product(req)

        self.mock_repo.create_product.return_value = None
        self.mock_repo.get_by_sku.return_value = None

        with self.assertRaises(ValueError) as context2:
            self.service.create_product(req)

        self.assertEqual(str(context1.exception), "sku is not unique")
        self.assertEqual(str(context2.exception), "sku is not unique")

    def test_create_product_brand_is_none(self):

        now = datetime.now(timezone.utc)

        req1 = CreateProductRequest(
            sku = 10,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = None
        )

        req2 = CreateProductRequest(
            sku = 10,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "  "
        )

        self.mock_repo.get_by_sku.return_value = None

        with self.assertRaises(ValueError) as context1:
            self.service.create_product(req1)

        self.assertEqual(str(context1.exception), "Brand is required")

        with self.assertRaises(ValueError) as context2:
            self.service.create_product(req2)

        self.assertEqual(str(context2.exception), "Brand is required")

    
    # Test cases for update_product function in service layer

    def test_update_product_success(self):
        now = datetime.now(timezone.utc)

        fake_product = ProductEntity(
            sku = 10,
            name = "updated_name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        )

        self.mock_repo.update_product.return_value = fake_product

        req = UpdateProductRequest(
            name = "updated_name",
            quantity = 100,
            reorder_level = 10,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        )

        result = self.service.update_product(10, req)

        self.assertIsNotNone(result)
        self.assertEqual(result.sku, fake_product.sku)
        self.assertEqual(result.created_at, fake_product.created_at)
        self.assertIsInstance(result, ProductResponse)

    def test_update_product_product_not_found(self):

        self.mock_repo.update_product.return_value = None

        req = UpdateProductRequest(
            name = "updated_name",
            quantity = 100,
            reorder_level = 10,
            updated_at = datetime.now(timezone.utc),
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        )

        result = self.service.update_product(10, req)

        self.assertIsNone(result)

    def test_update_product_sku_not_found(self):
        now = datetime.now(timezone.utc)

        req = UpdateProductRequest(
            name = "updated_name",
            quantity = 100,
            reorder_level = 10,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        )

        with self.assertRaises(ValueError) as context:
            self.service.update_product(None, req)

        self.assertEqual(str(context.exception), "sku is required")

       
    # Test cases for update_product function in service layer

    def test_delete_product_success(self):
        self.mock_repo.delete_product.return_value = True

        result = self.service.delete_product(10)

        self.assertIsNotNone(result)
        self.assertTrue(result)

    def test_delete_product_product_not_found(self):
        self.mock_repo.delete_product.return_value = False

        result = self.service.delete_product(10)

        self.assertIsNotNone(result)
        self.assertFalse(result)

    def test_delete_product_sku_not_found(self):
        
        with self.assertRaises(ValueError) as context:
            self.service.delete_product(None)

        self.assertEqual(str(context.exception), "sku is required")


    # Tests for list_products_of_category function in service layer

    def test_list_products_of_category_success(self):

        now = datetime.now(timezone.utc)

        fake_products = [ProductEntity(
            sku = 123 + i,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        ) for i in range(0,10)]

        self.mock_repo.get_products_of_category.return_value = fake_products

        result = self.service.list_products_of_category("69b395850bd8a1cdb72af391")

        self.assertIsNotNone(result)
        self.assertEqual([p.sku for p in result], [p.sku for p in fake_products])
        for p in result:
            self.assertEqual(p.category_id, "69b395850bd8a1cdb72af391")
            self.assertIsInstance(p, ProductResponse)
        self.mock_repo.get_products_of_category.assert_called_once_with("69b395850bd8a1cdb72af391")

    def test_list_products_of_category_category_does_not_exist(self):

        self.mock_repo.get_products_of_category.return_value = None

        result = self.service.list_products_of_category("69b395850bd8a1cdb72af391")

        self.assertIsNone(result)
        self.mock_repo.get_products_of_category.assert_called_once_with("69b395850bd8a1cdb72af391")

    def test_list_products_of_category_category_id_is_none(self):

        with self.assertRaises(ValueError) as context:
            self.service.list_products_of_category(None)

        self.assertEqual(str(context.exception), "Category is required")

    def test_list_products_of_category_empty_list(self):

        self.mock_repo.get_products_of_category.return_value = []

        result = self.service.list_products_of_category("69b395850bd8a1cdb72af391")

        self.assertIsNotNone(result) # result should be an empty list but should not be treated as None as that would indicate that the category does not exist
        self.assertEqual([], result) # In this case the category exists, it just does not ahve any products assigned to it

    
    # Tests for assign_category function in service layer

    def test_assign_category_success(self):

        now = datetime.now(timezone.utc)

        fake_product = ProductEntity(
            sku = 123,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69aec72934dd66b7db34a1ee",
            brand = "brand")

        self.mock_repo.add_category.return_value = fake_product

        result = self.service.assign_category(123, "69aec72934dd66b7db34a1ee")

        self.assertIsNotNone(result)
        self.assertEqual(result.sku, fake_product.sku)
        self.assertEqual(result.category_id, fake_product.category_id)

    def test_assign_category_sku_is_none(self):

        with self.assertRaises(ValueError) as context:
            self.service.assign_category(None, "69aec72934dd66b7db34a1ee")

        self.assertEqual(str(context.exception), "sku is required")

    def test_assign_category_category_id_is_none(self):

        with self.assertRaises(ValueError) as context:
            self.service.assign_category(123, None)

        self.assertEqual(str(context.exception), "Category is required")

    def test_assign_category_product_does_not_exist(self):

        self.mock_repo.add_category.return_value = None

        result = self.service.assign_category(123, "69aec72934dd66b7db34a1ee")

        self.assertIsNone(result)
        

    # Tests for remove_category function in service layer

    def test_remove_category_success(self):

        now = datetime.now(timezone.utc)

        fake_product = ProductEntity(
            sku = 123,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391", # if for Uncategorized products
            brand = "brand")
        
        self.mock_repo.remove_category.return_value = fake_product

        result = self.service.remove_category(123, "69aec72934dd66b7db34a1ee")

        self.assertIsNotNone(result)
        self.assertIsInstance(result, ProductResponse)
        self.assertEqual(result.sku, fake_product.sku)
        self.assertEqual(result.category_id, fake_product.category_id)

    def test_remove_category_sku_is_none(self):

        with self.assertRaises(ValueError) as context:
            self.service.remove_category(None, "69aec72934dd66b7db34a1ee")

        self.assertEqual(str(context.exception), "sku is required")

    def test_remove_category_category_id_is_none(self):

        with self.assertRaises(ValueError) as context:
            self.service.remove_category(123, None)

        self.assertEqual(str(context.exception), "Category is required")

    def test_remove_category_product_does_not_exist(self):
        
        self.mock_repo.remove_category.return_value = None

        result = self.service.remove_category(123, "69aec72934dd66b7db34a1ee")

        self.assertIsNone(result)
        
    # Tests for bulk_create_products function in service layer

    def test_bulk_create_products_success(self):

        now = datetime.now(timezone.utc)

        fake_products = [ProductEntity(
            sku = 10+i,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        ) for i in range(10)]

        self.mock_repo.bulk_create_products.return_value = fake_products
        self.mock_repo.get_by_sku.return_value = None

        req = [CreateProductRequest(
            sku = 10+i,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        ) for i in range(10)]

        result = self.service.bulk_create_products(req)

        self.assertIsNotNone(result)
        for p in result:
            self.assertIsInstance(p, ProductResponse)
        self.assertEqual([p.sku for p in result], [p.sku for p in fake_products])

    def test_bulk_create_products_csv_skus_not_unique(self):

        now = datetime.now(timezone.utc)

        req = [CreateProductRequest(
            sku = 10,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        ) for i in range(10)]

        self.mock_repo.get_by_sku.return_value = None

        with self.assertRaises(ValueError) as context:
            self.service.bulk_create_products(req)
        
        self.assertEqual(str(context.exception), "Multiple product with sku 10 found in csv file, sku must be unique")

    def test_bulk_create_products_sku_not_unique(self):

        now = datetime.now(timezone.utc)

        req = [CreateProductRequest(
            sku = 10 + i,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = "brand"
        ) for i in range(10)]

        self.mock_repo.get_by_sku.return_value = "Not Null Value"

        with self.assertRaises(ValueError) as context:
            self.service.bulk_create_products(req)
        
        self.assertEqual(str(context.exception), "Product with sku 10 already exists in database")

    def test_bulk_create_products_brand_is_none(self):

        now = datetime.now(timezone.utc)

        req1 = [CreateProductRequest(
            sku = 10 + i,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = None
        ) for i in range(10)]

        req2 = [CreateProductRequest(
            sku = 10 + i,
            name = "name",
            quantity = 100,
            reorder_level = 10,
            created_at = now,
            updated_at = now,
            category_id = "69b395850bd8a1cdb72af391",
            brand = ""
        ) for i in range(10)]

        self.mock_repo.get_by_sku.return_value = None

        with self.assertRaises(ValueError) as context1:
            self.service.bulk_create_products(req1)
        with self.assertRaises(ValueError) as context2:
            self.service.bulk_create_products(req2)
        
        self.assertEqual(str(context1.exception), "Product with sku 10 does not have a brand")
        self.assertEqual(str(context2.exception), "Product with sku 10 does not have a brand")

    def test_bulk_create_products_empty_list(self):

        self.mock_repo.bulk_create_products.return_value = []
        self.mock_repo.get_by_sku.return_value = None

        result = self.service.bulk_create_products([])

        self.assertIsNotNone(result)
        self.assertEqual(result, [])


        
if __name__ == "__main__":
    unittest.main()
        

        

        
    
    