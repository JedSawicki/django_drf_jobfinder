from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('__all__')
        

class CreateOfferSerializer(serializers.Serializer):
    key_words = serializers.CharField(max_length=50)