from django.db import models

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
    model = models.CharField(max_length=255)
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


class Rack(models.Model):
    rack = models.CharField(max_length=50)
    size_u = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.rack} - {self.size_u}U"


class System(models.Model):
    location = models.ForeignKey(Rack, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    cpu = models.ForeignKey(CPU, on_delete=models.SET_NULL, null=True, blank=True)
    ram = models.ManyToManyField(RAM, blank=True)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.SET_NULL, null=True, blank=True)
    nic = models.ManyToManyField(NIC, blank=True)
    psu = models.ForeignKey(PSU, on_delete=models.SET_NULL, null=True, blank=True)
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, blank=True)
    os_use_case = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.location} - {self.name}"
