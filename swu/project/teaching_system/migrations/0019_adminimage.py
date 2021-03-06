# Generated by Django 2.2.6 on 2019-12-05 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching_system', '0018_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('src', models.ImageField(upload_to='adminImage')),
            ],
            options={
                'db_table': 'adminImage',
            },
        ),
    ]
