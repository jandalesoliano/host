# Generated by Django 5.0.3 on 2024-03-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminUser', '0008_rename_application_id_usercredentials_application_idu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresult',
            name='vscore',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]