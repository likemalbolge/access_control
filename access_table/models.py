from django.db import models

class Employee(models.Model):
    employeeTerminalNo = models.IntegerField('Номер в терміналі')
    employeeName = models.CharField('Прізвище та ім\'я', max_length=200, unique=True)

    def __str__(self):
        return f'({self.employeeTerminalNo}) {self.employeeName}'

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        ordering = ['employeeTerminalNo']

class Record(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name='Працівник')
    acs_time = models.DateTimeField('Час події', blank=True, null=True)

    def __str__(self):
        return f'{self.employee.employeeName} - {self.acs_time}'

    class Meta:
        verbose_name='Запис з терміналу'
        verbose_name_plural='Записи з терміналу'
        ordering = ['acs_time']