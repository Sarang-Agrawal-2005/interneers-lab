from django.core.management.base import BaseCommand
from Products.repository.product_model import ProductModel
from Products.repository.product_category_model import ProductCategoryModel
from datetime import datetime, timezone

class Command(BaseCommand):
    help = "Migrate old products without a category to a default category"

    def handle(self, *args, **kwargs):
        products = ProductModel.objects(category = None)

        now = datetime.now(timezone.utc)

        uncategorized = ProductCategoryModel.objects(title="Uncategorized").first()
        if not uncategorized:
            uncategorized = ProductCategoryModel(
                title="Uncategorized",
                description="All products with no assigned category.",
                created_at=now,
                updated_at=now
            ).save()

        for p in products:
            p.category = uncategorized
            p.updated_at = now
            p.save()

        self.stdout.write(self.style.SUCCESS(f"Migrated {len(products)} old products"))
