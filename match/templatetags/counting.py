from django import template

register = template.Library()
@register.filter

def subtract(value,arg):
    return int(value) - int(arg)

def range(value):
    return range(0, value);