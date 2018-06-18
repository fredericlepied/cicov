from rest_framework import serializers
from cicovapp.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'created', 'name', 'version', 'inherit', 'url')
