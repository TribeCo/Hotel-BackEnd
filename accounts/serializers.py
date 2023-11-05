from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# -------------------------------------------------------------------------------------------------------------------------------
class EnhancedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phoneNumber'] = user.phoneNumber
        # ...
        return token
# -------------------------------------------------------------------------------------------------------------------------------
class UserSerializersValid(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nationalCode', 'phoneNumber']
# -------------------------------------------------------------------------------------------------------------------------------
class CodeValidationSerializers(serializers.ModelSerializer):
    phoneNumber = serializers.CharField()
    code = serializers.CharField()
    class Meta:
        model = User
        fields = ['phoneNumber', 'code']
# -------------------------------------------------------------------------------------------------------------------------------
