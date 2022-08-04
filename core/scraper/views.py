from rest_framework import generics
from .models import Offer
from .serializers import OfferSerializer


class OfferList(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    
    def get_queryset(self):
        queryset = Offer.objects.all()
        
        return queryset
        
        
class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()