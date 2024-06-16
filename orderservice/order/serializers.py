from rest_framework import serializers


class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_product_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Product ID must be a positive integer.")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product_id', 'quantity', 'total_price']

