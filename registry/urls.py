from django.urls import path,include
from .views import RegisterEntryView,TotalListView
urlpatterns = [
 path('entry/',RegisterEntryView.as_view()),
 path('list/',TotalListView.as_view()),
]