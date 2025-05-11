from django.db import models

class Rack(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()

    def __str__(self):
        return self.name


class Component(models.Model):
    COMPONENT_TYPES = [
        ('CPU', 'CPU'),
        ('RAM', 'RAM'),
        ('MOTHERBOARD', 'Motherboard'),
        ('STORAGE', 'Storage'),
        ('NIC', 'Network Interface Card'),
        ('PSU', 'Power Supply Unit'),
        ('CASE', 'Case'),
        ('OTHER', 'Other'),
    ]
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    model = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    link_justification = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.model}"


class System(models.Model):
    name = models.CharField(max_length=255)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name='systems')
    size = models.IntegerField(help_text="Size in rack units (U)")
    components = models.ManyToManyField(Component, blank=True, related_name='systems')

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        return sum(comp.unit_price for comp in self.components.all())