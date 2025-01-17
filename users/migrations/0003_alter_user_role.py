# Generated by Django 5.1.4 on 2025-01-02 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_date_of_birth_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(help_text='Роль', max_length=50, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.role', verbose_name='Роль'),
        ),
    ]
