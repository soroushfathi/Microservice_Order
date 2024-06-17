from .models import Order
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


def get_all_orders():
    return Order.objects.all()


def get_order_by_id(order_id):
    try:
        order = Order.objects.get(id=order_id)
        return order
    except Order.DoesNotExist:
        return None

