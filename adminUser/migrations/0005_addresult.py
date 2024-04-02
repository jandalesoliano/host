# Generated by Django 5.0.3 on 2024-03-24 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminUser', '0004_usercredentials_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verbalComprehension', models.IntegerField(blank=True, max_length=10, null=True)),
                ('verbalReasoning', models.IntegerField(blank=True, max_length=10, null=True)),
                ('figuralReasoning', models.IntegerField(blank=True, max_length=10, null=True)),
                ('qualitativeReasoning', models.IntegerField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]