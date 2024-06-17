import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import OpenApiExample, extend_schema

from orderservice.api.utils import format_response
from orderservice.utils.product_service import ProductService
from .services import create_order
from .selectors import get_order_by_id, get_all_orders
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from .producer import publish

logger = logging.getLogger(__name__)
product_service = ProductService()


class OrderCreateView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        request=OrderCreateSerializer,
        responses={201: OrderSerializer},
        examples=[
            OpenApiExample(
                'Example Input',
                value={
                    'product_id': 'ID of a product',
                    'quantity': 'Quantity of a product'
                }
            ),
        ],
    )
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            fresponse = format_response(
                success=False,
                message=serializer.errors,
            )
            return Response(fresponse, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        product = product_service.get_product(product_id=product_id)
        if not product['success']:
            fresponse = format_response(success=False,
                    message="Product Not Found")
            return Response(fresponse, statuss=status.HTTP_404_NOT_FOUND)

        product_data = product['data']
        product_stock = product_data['stock']
        product_price = float(product_data['price'])
        if quantity > product_stock:
            fresponse = format_response(success=False,
                    message="Not Available Stock for this product")
            return Response(fresponse, status=status.HTTP_400_BAD_REQUEST)

        order = create_order(product_id, product_price, quantity)

        # Update Product Stock
        productupdate_response = product_service.update_product_stock(
                product_data, quantity)
        logger.info("Update product stock result: %s" % (productupdate_response))

        # Test Rabbitmq
        # publish('create_order', product_data)

        order_serializer = OrderSerializer(order)
        fresponse = format_response(success=True,
                data=order_serializer.data,
                message="Order Has been created successfully.")
        return Response(fresponse, status=status.HTTP_200_OK)


class OrderListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            orders = get_all_orders()
            serializer = OrderSerializer(orders, many=True)
            fresponse = format_response(success=True, data=serializer.data)
            return Response (fresponse, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Exception of Get Order List: {e}")
            fresponse = format_response(success=False, message=str(e))
            return Response(fresponse, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, orderid):
        try:
            order = get_order_by_id(orderid)
            if order is None:
                response_data = format_response(success=False, message="Order Not Found")
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(order)
            response_data = format_response(success=True, data=serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Exception in Get order detail: {e}")
            response_data = format_response(success=False, message=str(e), error_code=500)
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

