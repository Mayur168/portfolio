# Generated by Django 5.2.3 on 2025-06-20 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Mobile Number'),
        ),
    ]
