from django import template
import datetime

register = template.Library()
@register.filter

def subtract(value,arg):
    return int(value) - int(arg)

def strToInt(value):
    return int(value);

@register.filter
def hourDifference(value):
    now = datetime.datetime.now()
    delta = value - now
    
    return int(delta.seconds)/3600
    
@register.filter
def dayDifference(value):
    now = datetime.datetime.now()
    delta = value - now
    
    return int(delta.days)

@register.filter
def hourMinute(value):
    hour = value[0:2]
    minute = value[2:4]
    
    return hour + ':' + minute
