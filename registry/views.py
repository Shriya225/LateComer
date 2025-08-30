from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LatecomerSerializer,TotalListSerializer
from .models import LateEntry,Student
from .serializers import TotalListSerializer,StudentSerializer
from .filters import LateEntryFilter
from rest_framework.views import APIView
from django.http import HttpResponse
import openpyxl
from io import BytesIO
from django.db.models import Count,Q
class RegisterEntryView(APIView):
    def post(self,request):
        serilaizer=LatecomerSerializer(data=request.data)
        if serilaizer.is_valid():
            obj=serilaizer.save()
            ans=LatecomerSerializer(obj)
            return Response(ans.data)
        return Response(serilaizer.errors)



from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response

class TotalListView(APIView):
    def get(self, request):
        # Step 1: Get filtered late entries
        late_entries = LateEntryFilter(request.GET, queryset=LateEntry.objects.all()).qs

        # Step 2: Extract student ids from filtered entries
        student_ids = late_entries.values_list("student_id", flat=True).distinct()
        print(student_ids)
        # Step 3: Fetch those students and annotate with total all-time count
        students = (
            Student.objects.filter(id__in=student_ids)
            .annotate(total_count=Count("late_entries"))  # count across ALL late_entries
        )

        # Step 4: Serialize
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)



class LateEntryDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Step 1: Get filtered late entries (decides which students appear)
        late_entries = LateEntryFilter(request.GET, queryset=LateEntry.objects.all()).qs
        student_ids = late_entries.values_list("student_id", flat=True).distinct()

        # Step 2: Fetch those students with lifetime late entry counts
        students = (
            Student.objects.filter(id__in=student_ids)
            .annotate(total_count=Count("late_entries"))  # lifetime count
        )

        # Step 3: Create Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        date = request.GET.get("date")  # from query params
        if date:
            ws.title = f"Late Entries on {date}"
        else:
            ws.title = "Late Entries"

        # Header row
        ws.append(['Roll No', 'Name', 'Year', 'Branch', 'Course', 'Total Late Entries'])

        # Data rows
        for student in students:
            ws.append([
                student.roll_no,
                student.name,
                student.year,
                student.branch,
                student.course,
                student.total_count
            ])

        # Step 4: Prepare response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=late_entries{date}.xlsx'
        wb.save(response)
        return response


    