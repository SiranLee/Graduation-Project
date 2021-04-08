# Generated by Django 2.2.6 on 2019-12-01 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teaching_system', '0014_auto_20191201_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cs',
            field=models.CharField(default='', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='teaching_system.Department'),
            preserve_default=False,
        ),
    ]