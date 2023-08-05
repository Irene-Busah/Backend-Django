from rest_framework import serializers
from .models import MenuItem, Category
import bleach


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    # ================= Validating the user inputs - PART 1 ===================
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)

    # ================= Validating the user inputs - PART 2 ===================
    # def validate_title(self, value):
    #     return bleach.clean(value)
    
    # def validate_price(self, value):
    #     if (value < 2):
    #         raise serializers.ValidationError('Price must not be less than 2.0')
    
    # def validate_inventory(self, value):
    #     if (value < 0):
    #         raise serializers.ValidationError('Inventory must be greater than 0')

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory', 'category', 'category_id']
        # this is another way for setting validations on the different fields.
        # extra_kwargs = {
        #     'price': {'min_value': 2},
        #     'inventory': {'min_value': 0}
        # }