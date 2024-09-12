from django.urls import path
from .views import ImageAPIView, ImageTransformationAPIView

urlpatterns = [
    path('', ImageAPIView.as_view(), name='images'),
    path('<int:pk>/transform/', ImageTransformationAPIView.as_view(), name="transform")
]