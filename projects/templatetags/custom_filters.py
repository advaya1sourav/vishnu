# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """Returns the value of the dictionary for the given key."""
    return dictionary.get(key)
