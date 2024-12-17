from datetime import datetime
from django.contrib import admin
from .models import Employee, Record
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

admin.site.site_header = 'Адміністрування контролю доступу'
admin.site.site_title = 'Адміністрування контролю доступу'
admin.site.index_title = 'Контроль доступу'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employeeTerminalNo', 'employeeName')

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'acs_time')
    list_filter = (('employee', RelatedDropdownFilter), ('acs_time', DateRangeQuickSelectListFilterBuilder(title='часом події',
                                                                                  default_start=datetime.today(),
                                                                                  default_end=datetime.today())))
