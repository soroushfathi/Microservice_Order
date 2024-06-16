from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from orderservice.api.utils import format_response
from orderservice.utils.product_service import ProductService
from .serializers import OrderCreateSerializer


product_service = ProductService()


class CreateOrder(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            fresponse = format_response(
                success=False,
                message=serializer.errors,
            )
            return Response(fresponse, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializers.validated_data['product_id']
        quantity = serializers.validated_data['quantity']
        product = product_service.get_product(product_id=product_id)
        if not product['status']:
            fresponse = format_response(success=False,
                    message="Product Not Found")
            return Response(fresponse, statuss=status.HTTP_404_NOT_FOUND)

        product_data = product['data']
        if quantity > product_data['stock']:
            fresponse = format_response(success=False,
                    message="Not Available Stock for this product")
            return Response(fresponse, status=status.HTTP_400_BAD_REQUEST)

        total_price = quantity * float(product_data['price'])

        # Save Order
        ...
