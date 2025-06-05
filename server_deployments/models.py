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
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.model} ({self.cores}C/{self.threads}T)"


class RAM(models.Model):
    size_gb = models.PositiveIntegerField()
    speed_mhz = models.PositiveIntegerField()
    ecc = models.BooleanField(default=False)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.size_gb}GB {self.speed_mhz}MHz {'ECC' if self.ecc else 'Non-ECC'}"


class Motherboard(models.Model):
    model = models.CharField(max_length=255)
    socket = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=50)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model


class NIC(models.Model):
    model = models.CharField(max_length=255)
    speed_gbps = models.PositiveIntegerField()
    port_count = models.PositiveIntegerField()
    interface_type = models.CharField(max_length=50, choices=[('SFP+', 'SFP+'), ('RJ45', 'RJ45')])
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.model} {self.speed_gbps}Gbps {self.interface_type}"


class PSU(models.Model):
    model = models.CharField(max_length=255)
    wattage = models.PositiveIntegerField()
    efficiency_rating = models.CharField(max_length=50)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.model} {self.wattage}W {self.efficiency_rating}"


class Case(models.Model):
    model = models.CharField(max_length=255)
    form_factor = models.CharField(max_length=50)
    drive_bays = models.CharField(max_length=255)
    expansion_slots = models.PositiveIntegerField()
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model


class StorageDevice(models.Model):
    model = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    storage_type = models.CharField(max_length=10, choices=[('HDD', 'HDD'), ('SSD', 'SSD'), ('NVMe', 'NVMe')])
    capacity_gb = models.PositiveIntegerField()
    rpm = models.PositiveIntegerField(blank=True, null=True)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

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
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.location} - {self.name}"
    

class MovieIndex(models.Model):
    system = models.ForeignKey('System', on_delete=models.CASCADE, related_name='movie_indexes')
    name = models.CharField(max_length=255)  # e.g., 'Inception'
    path = models.TextField(unique=True)
    file_count = models.IntegerField()
    folder_size_bytes = models.BigIntegerField()
    last_scanned = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class TVShowIndex(models.Model):
    system = models.ForeignKey('System', on_delete=models.CASCADE, related_name='tv_show_indexes')
    name = models.CharField(max_length=255)  # e.g., 'Breaking Bad'
    path = models.TextField(unique=True)
    season_count = models.IntegerField()
    total_size_bytes = models.BigIntegerField()
    last_scanned = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

class SeasonIndex(models.Model):
    tv_show = models.ForeignKey(TVShowIndex, on_delete=models.CASCADE, related_name='seasons')
    name = models.CharField(max_length=255)         # e.g., 'Season 1'
    path = models.TextField(unique=True)
    file_count = models.IntegerField()
    folder_size_bytes = models.BigIntegerField()

    def __str__(self):
        return f"{self.tv_show.name} - {self.name}"


class MediaFile(models.Model):
    path = models.TextField(unique=True)
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    size_bytes = models.BigIntegerField()

    movie = models.ForeignKey('MovieIndex', on_delete=models.CASCADE, null=True, blank=True, related_name='files')
    season = models.ForeignKey('SeasonIndex', on_delete=models.CASCADE, null=True, blank=True, related_name='files')

    def __str__(self):
        return self.name
