# Generated by Django 2.1.5 on 2019-01-28 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0004_auto_20190127_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashproject',
            name='description',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='noncashproject',
            name='description',
            field=models.TextField(max_length=300),
        ),
    ]
