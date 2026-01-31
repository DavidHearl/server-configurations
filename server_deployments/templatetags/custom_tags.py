from django import template
register = template.Library()

@register.filter
def to(value, end):
    return range(value, end + 1)

@register.filter
def free_space_gb(capacity_tb, utilisation):
    """Calculate free space in GB given capacity in TB and utilisation percentage"""
    if capacity_tb is None or utilisation is None:
        return 0
    total_gb = capacity_tb * 1000
    used_gb = total_gb * (utilisation / 100)
    free_gb = total_gb - used_gb
    return int(free_gb)
