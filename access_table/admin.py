from datetime import datetime

from django.contrib import admin
from .models import Employee, Record
from rangefilter.filters import DateRangeFilterBuilder

admin.site.site_header = 'Адміністрування контролю доступу'
admin.site.site_title = 'Адміністрування контролю доступу'
admin.site.index_title = 'Контроль доступу'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employeeTerminalNo', 'employeeName')

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'acs_time')
    list_filter = ('employee', ('acs_time', DateRangeFilterBuilder(title='Час події',
                                                                   default_start=datetime(2024, 12, 1),
                                                                   default_end=datetime(2024, 12, 31))))
