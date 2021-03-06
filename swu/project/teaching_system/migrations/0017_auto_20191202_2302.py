# Generated by Django 2.2.6 on 2019-12-02 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching_system', '0016_auto_20191201_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('src', models.ImageField(upload_to='studentImage')),
            ],
            options={
                'db_table': 'studentImage',
            },
        ),
        migrations.CreateModel(
            name='TeacherImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('src', models.ImageField(upload_to='teacherImage')),
            ],
            options={
                'db_table': 'teacherImage',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.TextField(default='/upfile/template/icon.jpg'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.TextField(default='/upfile/template/icon.jpg'),
            preserve_default=False,
        ),
    ]
