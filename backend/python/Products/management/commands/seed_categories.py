from django.core.management.base import BaseCommand
from Products.repository.product_category_model import ProductCategoryModel
from datetime import datetime, timezone

DEFAULT_CATEGORIES = [
    ("Food items", "All food items and snacks."),
    ("Clothes", "Clothing items."),
    ("Books and Magazines", "Literary works."),
    ("Electronics", "All kinds of electrical appliances."),
    ("Uncategorized", "All products with no assigned category.")
]

class Command(BaseCommand):
    help = "Predefined seed categories for Products"

    def handle(self, *args, **kwargs):
        now = datetime.now(timezone.utc)

        for title, description in DEFAULT_CATEGORIES:
            exists = ProductCategoryModel.objects(title = title).first()

            if not exists:
                ProductCategoryModel(
                    title = title,
                    description = description,
                    created_at = now,
                    updated_at = now
                ).save()
                self.stdout.write(self.style.SUCCESS(f"Created: {title}"))
            else:
                self.stdout.write(f"Already exists: {title}")

