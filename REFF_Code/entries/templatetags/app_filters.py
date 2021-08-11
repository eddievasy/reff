# This is a custom filter to allow us to use dictionaries in our templates

from django import template

register = template.Library()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)