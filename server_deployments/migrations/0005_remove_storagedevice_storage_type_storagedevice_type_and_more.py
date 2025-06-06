# Generated by Django 5.2.1 on 2025-05-12 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_deployments', '0004_storagedevice_storagetype_remove_system_os_use_case_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storagedevice',
            name='storage_type',
        ),
        migrations.AddField(
            model_name='storagedevice',
            name='type',
            field=models.CharField(choices=[('HDD', 'HDD'), ('SSD', 'SSD'), ('NVMe', 'NVMe')], default=1, max_length=10, unique=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='StorageType',
        ),
    ]
