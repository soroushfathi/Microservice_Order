from django.db import models


class Order(models.Model):
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order of {self.quantity} units of product ID {self.product_id}"

