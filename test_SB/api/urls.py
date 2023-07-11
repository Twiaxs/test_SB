from django.urls import path
from api.views import DealUploadView

urlpatterns = [
    path('api/deals/', DealUploadView.as_view(), name='deal-upload'),
]