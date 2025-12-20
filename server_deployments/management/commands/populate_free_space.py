from django.core.management.base import BaseCommand
from server_deployments.models import StorageDevice

class Command(BaseCommand):
    help = 'Populate free_space_gb field for existing StorageDevice records'

    def handle(self, *args, **options):
        devices = StorageDevice.objects.all()
        updated_count = 0

        for device in devices:
            if device.capacity_tb and device.utilisation is not None:
                total_gb = device.capacity_tb * 1000
                used_gb = total_gb * (device.utilisation / 100)
                free_gb = total_gb - used_gb
                device.free_space_gb = int(free_gb)
                device.save(update_fields=['free_space_gb'])
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} StorageDevice records with free_space_gb values')
        )