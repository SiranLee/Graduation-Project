# Generated by Django 2.2.6 on 2019-11-29 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teaching_system', '0006_file_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='dno',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='teaching_system.Department'),
            preserve_default=False,
        ),
    ]
