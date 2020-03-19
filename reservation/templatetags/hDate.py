from django import template

register = template.Library()
@register.filter

def hDate(value):
    return value[0:2] + "월 " + value[2:4] + "일"