from django.db import models
from django.utils.timezone import now

class CPU(models.Model):
    model = models.CharField(max_length=255)
    cores = models.PositiveIntegerField()
    threads = models.PositiveIntegerField()
    base_clock_ghz = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    wattage = models.PositiveIntegerField()
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    owned = models.IntegerField()

    def __str__(self):
        return f"{self.model} ({self.cores}C/{self.threads}T)"


class RAM(models.Model):
    size_gb = models.PositiveIntegerField()
    speed_mhz = models.PositiveIntegerField()
    ecc = models.BooleanField(default=False)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    owned = models.IntegerField()

    def __str__(self):
        return f"{self.size_gb}GB {self.speed_mhz}MHz {'ECC' if self.ecc else 'Non-ECC'}"


class Motherboard(models.Model):
    model = models.CharField(max_length=255)
    socket = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=50)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    owned = models.IntegerField()

    def __str__(self):
        return self.model


class NIC(models.Model):
    model = models.CharField(max_length=255)
    speed_gbps = models.PositiveIntegerField()
    port_count = models.PositiveIntegerField()
    interface_type = models.CharField(max_length=50, choices=[('SFP+', 'SFP+'), ('RJ45', 'RJ45')])
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    owned = models.IntegerField()

    def __str__(self):
        return f"{self.model} {self.speed_gbps}Gbps {self.interface_type}"


class PSU(models.Model):
    model = models.CharField(max_length=255)
    wattage = models.PositiveIntegerField()
    efficiency_rating = models.CharField(max_length=50)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    owned = models.IntegerField()

    def __str__(self):
        return f"{self.model} {self.wattage}W {self.efficiency_rating}"
    

class GPU(models.Model):
    model = models.CharField(max_length=255)
    cores = models.PositiveIntegerField()
    vram = models.PositiveIntegerField()
    vram_type = models.CharField(max_length=64)
    bus_width = models.PositiveIntegerField()
    link = models.URLField(blank=True, null=True)
    owned = models.IntegerField()

    def __str__(self):
        return f"{self.model} ({self.vram_gb}GB VRAM, {self.chipset})"


class HBA(models.Model):
    model = models.CharField(max_length=255)
    internal_connectors = models.IntegerField()
    external_connectors = models.IntegerField()
    connector_type = models.CharField(max_length=255)
    speed = models.CharField(max_length=255)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    owned = models.IntegerField()

    def __str__(self):
        return self.model


class Case(models.Model):
    model = models.CharField(max_length=255)
    form_factor = models.CharField(max_length=50)
    drive_bays = models.CharField(max_length=255)
    expansion_slots = models.PositiveIntegerField()
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    owned = models.IntegerField()

    def __str__(self):
        return self.model


class StorageDevice(models.Model):
    disk_number = models.PositiveIntegerField(null=True, blank=True)
    disk_position = models.PositiveIntegerField(null=True, blank=True)
    model = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    storage_type = models.CharField(max_length=10, choices=[('HDD', 'HDD'), ('SSD', 'SSD'), ('NVMe', 'NVMe')])
    storage_sub_type = models.CharField(max_length=255, null=True, blank=True)
    capacity_tb = models.PositiveIntegerField()
    rpm = models.PositiveIntegerField(blank=True, null=True)
    failure = models.BooleanField(default=False)
    cache = models.BooleanField(default=False)
    parity = models.BooleanField(default=False)
    utilisation = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Percentage of drive used")
    free_space_gb = models.PositiveIntegerField(null=True, blank=True, help_text="Free space in GB")
    actual_fragmentation = models.PositiveIntegerField(null=True, blank=True)
    ideal_fragmentation = models.PositiveIntegerField(null=True, blank=True)
    fragmentation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Fragmentation percentage")
    fragmentation_last_updated = models.DateTimeField(null=True, blank=True, help_text="Last time fragmentation data was updated")

    def __str__(self):
        rpm_str = f", {self.rpm}RPM" if self.rpm else ""
        return f"{self.model}-{self.serial_number}"


class Rack(models.Model):
    rack = models.CharField(max_length=50)
    size_u = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.rack} - {self.size_u}U"


class System(models.Model):
    rack_units = models.IntegerField()
    location = models.ForeignKey(Rack, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cpu = models.ForeignKey(CPU, on_delete=models.SET_NULL, null=True, blank=True)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.SET_NULL, null=True, blank=True)
    ram = models.ForeignKey(RAM, on_delete=models.SET_NULL, null=True, blank=True)
    ram_qty = models.PositiveIntegerField(default=1)
    nic = models.ForeignKey(NIC, on_delete=models.SET_NULL, null=True, blank=True)
    psu = models.ForeignKey(PSU, on_delete=models.SET_NULL, null=True, blank=True)
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, blank=True)
    storage_devices = models.ManyToManyField(StorageDevice, blank=True)

    def __str__(self):
        return f"{self.id}: {self.location} - {self.name}"
    

# class IndexedFolder(models.Model):
#     system = models.ForeignKey(System, on_delete=models.CASCADE)
#     path = models.TextField(unique=True)  # e.g. "/mnt/user/data/exports"
#     total_size = models.BigIntegerField(default=0)
#     last_scanned = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return self.path


# class IndexedFile(models.Model):
#     system = models.ForeignKey(System, on_delete=models.CASCADE)
#     folder = models.ForeignKey(IndexedFolder, on_delete=models.CASCADE, related_name='files')
#     full_path = models.TextField(unique=True)  # e.g. "/mnt/user/data/exports/file.json"
#     filename = models.CharField(max_length=255)
#     file_size = models.BigIntegerField()
#     file_type = models.CharField(max_length=100, blank=True)  # e.g. "zip", "cfg", "mkv"
#     last_scanned = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return self.full_path


