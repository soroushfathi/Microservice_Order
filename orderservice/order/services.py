from .models import Order
from decimal import Decimal
import requests


def create_order(product_id: int, product_price: float, quantity: int):
    total_price = quantity * product_price

    order = Order.objects.create(
        product_id=product_id,
        quantity=quantity,
        total_price=Decimal(total_price)
    )
    return order

