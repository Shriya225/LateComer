from django.urls import path,include
from .views import Demo,CustomTokenObtainPairView,CustomTokenRefreshView,LogoutView
urlpatterns = [

path('login/',CustomTokenObtainPairView.as_view()),
path('refresh/',CustomTokenRefreshView.as_view()),
path('logout/',LogoutView.as_view()),
path('demo/',Demo.as_view()),
]
