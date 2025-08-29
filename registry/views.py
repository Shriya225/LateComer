from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LatecomerSerializer
class RegisterEntryView(APIView):
    def post(self,request):
        serilaizer=LatecomerSerializer(data=request.data)
        if serilaizer.is_valid():
            obj=serilaizer.save()
            ans=LatecomerSerializer(obj)
            return Response(ans.data)
        return Response(serilaizer.errors)
        