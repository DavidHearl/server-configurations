# Generated by Django 5.2.1 on 2025-06-05 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_deployments', '0015_rename_connectors_hba_connector_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storagedevice',
            old_name='capacity_gb',
            new_name='capacity_tb',
        ),
    ]
