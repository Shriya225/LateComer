from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LatecomerSerializer,TotalListSerializer
from .models import LateEntry
from .serializers import TotalListSerializer
from .filters import LateEntryFilter
class RegisterEntryView(APIView):
    def post(self,request):
        serilaizer=LatecomerSerializer(data=request.data)
        if serilaizer.is_valid():
            obj=serilaizer.save()
            ans=LatecomerSerializer(obj)
            return Response(ans.data)
        return Response(serilaizer.errors)

class TotalListView(APIView):
    def get(self,req):
        queryset=LateEntry.objects.all()
        filterset = LateEntryFilter(req.GET, queryset=queryset)
        s=TotalListSerializer(filterset.qs,many=True)
        return Response(s.data)
    
        