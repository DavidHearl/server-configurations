# Generated by Django 5.2.1 on 2025-06-06 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_deployments', '0018_indexedfolder_indexedfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexedfolder',
            name='total_size',
            field=models.BigIntegerField(default=0),
        ),
    ]
