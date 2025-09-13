from django.urls import path,include
from .views import Demo,CustomTokenObtainPairView,CustomTokenRefreshView,logout
urlpatterns = [

path('login/',CustomTokenObtainPairView.as_view()),
path('refresh/',CustomTokenRefreshView.as_view()),
path('logout/',logout),
path('demo/',Demo.as_view()),
]
