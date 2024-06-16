from .models import Order
from decimal import Decimal
import requests

def get_product_price(product_id):
    # Placeholder function to simulate retrieving product price from the product service
    # In a real implementation, this would make an API call to the product service and retrieve the price.
    # Example:
    response = requests.get(f"http://productservice/api/products/{product_id}/")
    response_data = response.json()
    return Decimal(response_data['price'])


def create_order(data):
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    product_price = get_product_price(product_id)
    total_price = quantity * product_price

    order = Order.objects.create(
        product_id=product_id,
        quantity=quantity,
        total_price=total_price
    )
    return order

