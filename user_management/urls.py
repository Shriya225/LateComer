from django.urls import path,include
from .views import Demo,CustomTokenObtainPairView
urlpatterns = [

path('login/',CustomTokenObtainPairView.as_view()),
path('demo/',Demo.as_view()),
]
