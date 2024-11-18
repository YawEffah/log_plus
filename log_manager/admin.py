from django.contrib import admin

from .models import AttendanceRecord, Employee, Department

# Register your models here.


admin.site.register(AttendanceRecord)
admin.site.register(Employee)
admin.site.register(Department)
