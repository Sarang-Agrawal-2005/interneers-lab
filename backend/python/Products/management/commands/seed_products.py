from django.core.management.base import BaseCommand
from Products.repository.product_model import ProductModel
from Products.repository.product_category_model import ProductCategoryModel
from datetime import datetime, timezone

DEFAULT_PRODUCTS = [
    # FOOD
    (1, "Potato Chips", 120, 20, "69aec65b34dd66b7db34a1eb", "Layzone"),
    (2, "Instant Noodles", 200, 30, "69aec65b34dd66b7db34a1eb", "QuickBite"),

    # CLOTHES
    (3, "Basic T-Shirt", 75, 15, "69aec6a634dd66b7db34a1ec", "CottonWear"),
    (4, "Winter Jacket", 40, 10, "69aec6a634dd66b7db34a1ec", "WarmFit"),

    # BOOKS
    (5, "The Great Novel", 50, 10, "69aec6e934dd66b7db34a1ed", "Penguin"),
    (6, "Tech Magazine Vol. 12", 90, 15, "69aec6e934dd66b7db34a1ed", "TechWorld"),

    # ELECTRONICS
    (7, "Bluetooth Earbuds", 35, 8, "69aec72934dd66b7db34a1ee", "SoundMax"),
    (8, "Smartphone Charger", 150, 25, "69aec72934dd66b7db34a1ee", "VoltCharge"),

    # UNCATEGORIZED
    (9, "Mystery Box Item", 10, 5, "69b395850bd8a1cdb72af391", "Unknown"),
    (10, "Generic Household Item", 60, 10, "69b395850bd8a1cdb72af391", "HomeCo"),

    # TOYS
    (11, "Action Figure", 80, 15, "69ad291ed4ad7751156e2c01", "HeroMax"),
    (12, "Building Blocks Set", 120, 20, "69ad291ed4ad7751156e2c01", "BlockWorld")
]

class Command(BaseCommand):
    help = "Predefined seed categories for Products"

    def handle(self, *args, **kwargs):

        for sku, name, quantity, reorder_level, category_id, brand in DEFAULT_PRODUCTS:
            exists = ProductModel.objects(sku = sku).first()

            if not exists:
                
                now = datetime.now(timezone.utc)

                ProductModel(
                    sku = sku,
                    name = name,
                    quantity = quantity,
                    reorder_level = reorder_level,
                    created_at = now,
                    updated_at = now,
                    category = ProductCategoryModel.objects(id = category_id).first(),
                    brand = brand
                ).save()
                self.stdout.write(self.style.SUCCESS(f"Created: {sku}"))
            else:
                self.stdout.write(f"Already exists: {sku}")

