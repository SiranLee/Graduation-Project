# Generated by Django 2.2.6 on 2019-12-05 15:12

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('teaching_system', '0017_auto_20191202_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.CharField(max_length=10, unique=True)),
                ('aname', models.CharField(max_length=16)),
                ('image', models.TextField()),
                ('password', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'admin',
            },
            managers=[
                ('adminManage', django.db.models.manager.Manager()),
            ],
        ),
    ]