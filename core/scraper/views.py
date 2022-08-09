from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Offer
from .serializers import OfferSerializer, CreateOfferSerializer
from .worker import Scraper


class OfferList(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    
    def get_queryset(self):
        queryset = Offer.objects.all()
        
        return queryset
       
        
class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    
    
class CreateOfferList(APIView):
    serializer_class = CreateOfferSerializer
    # def get(self, request, format=None):
    #     offers = ScraperModel.objects.all()
    #     serializer_class = OfferSerializer(offers, many=True)
    #     return Response({"offers": serializer_class.data})
        
    def post(self, request, format=None):
        scrapy = Scraper()
        serializer_class = CreateOfferSerializer(data=request.data)
        if serializer_class.is_valid():
            key_words = serializer_class.data.get('key_words')
            print(key_words)
            key_list = []
            keys = key_words.split()
            for key in keys:
                key_list.append(key)
            while len(key_list) != 4:
                key_list.append(None)
            try:
                offers = scrapy.grand_scraper(key_list[0], key_list[1], key_list[2])
            except IndexError:
                pass
        
        return Response({"offers": offers})
    

            