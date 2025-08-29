from rest_framework import serializers
from .models import LateEntry, Student
from datetime import date

class LatecomerSerializer(serializers.ModelSerializer):
    roll_no = serializers.CharField(write_only=True)  # Accept roll_no in request
    total_count=serializers.SerializerMethodField()
    student_details=serializers.SerializerMethodField()
    class Meta:
        model = LateEntry
        fields = ['roll_no', 'reason', 'date','total_count','student_details']

    def create(self, validated_data):
        roll_no = validated_data.pop('roll_no')
        date_value = validated_data.get('date', date.today())
        try:
            student = Student.objects.get(roll_no=roll_no)
        except Student.DoesNotExist:
            raise serializers.ValidationError({"roll_no": "Student with this roll number does not exist."})
        
        if LateEntry.objects.filter(student=student, date=date_value).exists():
            raise serializers.ValidationError({
                "non_field_errors": f"Late entry for student {roll_no} on {date_value} already exists."
            })
        late_entry = LateEntry.objects.create(
            student=student,
            **validated_data
        )
        return late_entry
    def get_total_count(self,obj):
        return LateEntry.objects.filter(student=obj.student).count()
    def get_student_details(self,obj):
        student=obj.student
        return {
            "name": student.name,
            "branch": student.branch,
            "year": student.year,
            "course": student.course
        }

class TotalListSerializer(serializers.ModelSerializer):
    class Meta:
        model=LateEntry
        fields=["student","date","reason"]
        depth=1