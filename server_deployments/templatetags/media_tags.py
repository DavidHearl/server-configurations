from django import template
from django.utils.timesince import timesince
from django.utils.timezone import now

register = template.Library()

@register.filter
def scanned_ago(value):
    delta = now() - value
    if delta.days == 0:
        return "<1 day ago"
    return f"{timesince(value).split(',')[0]} ago"
