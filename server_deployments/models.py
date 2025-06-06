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
    model = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    storage_type = models.CharField(max_length=10, choices=[('HDD', 'HDD'), ('SSD', 'SSD'), ('NVMe', 'NVMe')])
    capacity_tb = models.PositiveIntegerField()
    rpm = models.PositiveIntegerField(blank=True, null=True)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)

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
        return f"{self.location} - {self.name}"
    
