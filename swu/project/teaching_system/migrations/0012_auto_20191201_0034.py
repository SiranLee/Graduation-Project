# Generated by Django 2.2.6 on 2019-11-30 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching_system', '0011_studentstore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mclass',
            name='cname',
            field=models.CharField(max_length=39),
        ),
    ]
