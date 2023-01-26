from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Offer
from .serializers import OfferSerializer, CreateOfferSerializer
from .worker.worker import Scraper


class OfferList(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    
    def get_queryset(self):
        queryset = Offer.objects.all()
        
        return queryset
       
        
class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    
    
class CreateOfferList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'job_scraper.html'
    offers = None
    
    def get(self, request):
        serializer = CreateOfferSerializer()
        return Response({'serializer': serializer})
        
    def post(self, request, format=None):
        scrapy = Scraper()
        serializer = CreateOfferSerializer(data=request.data)
        offers = None
        if serializer.is_valid():
            key_words = serializer.data.get('key_words')
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
        
        return Response({"serializer": serializer, "offers": offers})
    

