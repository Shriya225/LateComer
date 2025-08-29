from django.urls import path,include
from .views import RegisterEntryView
urlpatterns = [
 path('entry/',RegisterEntryView.as_view()),
]