from django.urls import path

from . import views
from .views import OfferList, OfferDetail

urlpatterns = [
    path('offers/', OfferList.as_view(), name='offers'),
    path('offers/<int:pk>/', OfferDetail.as_view(), name='offerDetail')
]