from django.db import models

class Employees(models.Model):
    employeeTerminalNo = models.IntegerField('Номер в терміналі')
    employeeName = models.CharField('Прізвище та ім\'я', max_length=200, unique=True)

    def __str__(self):
        return f'({self.employeeTerminalNo}) {self.employeeName}'

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        ordering = ['employeeTerminalNo']