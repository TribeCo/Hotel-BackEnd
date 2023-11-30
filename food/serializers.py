from rest_framework import serializers
from .models import *
# -------------------------------------------------------------------------------------------------------------------------------
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('price', 'name', 'meal', 'type', 'count')
# -------------------------------------------------------------------------------------------------------------------------------
