from django.contrib import admin
from .models import Employee, Record

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employeeTerminalNo', 'employeeName')

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'acs_time')
    list_filter = ('employee', 'acs_time')
