from django import template

register = template.Library()
@register.filter

def hDate(value):
    return value[4:6] + "월 " + value[6:8] + "일"