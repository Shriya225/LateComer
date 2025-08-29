from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LatecomerSerializer,TotalListSerializer
from .models import LateEntry
from .serializers import TotalListSerializer
from .filters import LateEntryFilter
from rest_framework.views import APIView
from django.http import HttpResponse
import openpyxl
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
    


class LateEntryDownloadView(APIView):
    def get(self, request):
        # Filter queryset
        queryset = LateEntryFilter(request.GET, queryset=LateEntry.objects.all()).qs

        # Create workbook in memory
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Late Entries"

        # Header
        ws.append(['Roll No', 'Name', 'Year', 'Branch', 'Course', 'Date', 'Reason'])

        # Data rows
        for entry in queryset:
            ws.append([
                entry.student.roll_no,
                entry.student.name,
                entry.student.year,
                entry.student.branch,
                entry.student.course,
                entry.date.strftime('%Y-%m-%d'),
                entry.reason or ""
            ])

        # Prepare response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=late_entries.xlsx'
        wb.save(response)  
        return response

        