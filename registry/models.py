from django.db import models
import uuid
from datetime import date

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        abstract = True  

class Student(UUIDModel):
    roll_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    YEAR_CHOICES = [(i, f"Year {i}") for i in range(1, 5)]
    year = models.IntegerField(choices=YEAR_CHOICES)
    COURSE_CHOICES = [
        ('B.Tech', 'B.Tech'),
        ('M.Tech', 'M.Tech'),
        ('MBA', 'MBA'),
    ]
    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('ECE', 'Electronics & Communication'),
        ('CIVIL', 'Civil Engineering'),
    ]
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    def __str__(self):
        return f"{self.roll_no} - {self.name}"
    

class LateEntry(UUIDModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='late_entries')
    date = models.DateField(default=date.today)
    # arrival_time = models.TimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.student.roll_no} - {self.date} "




