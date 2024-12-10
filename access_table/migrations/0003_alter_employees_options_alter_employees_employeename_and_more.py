# Generated by Django 5.1.4 on 2024-12-10 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_table', '0002_remove_employees_employeestatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employees',
            options={'ordering': ['employeeNoString'], 'verbose_name': 'Працівник', 'verbose_name_plural': 'Працівники'},
        ),
        migrations.AlterField(
            model_name='employees',
            name='employeeName',
            field=models.CharField(max_length=200, verbose_name="Прізвище та ім'я"),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employeeNoString',
            field=models.IntegerField(max_length=50, verbose_name='Номер в терміналі'),
        ),
    ]
