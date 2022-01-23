from django import template

register = template.Library()

@register.filter()
def increment(value):
    print(value)
    print(int(value)+1)
    return int(value)+1

@register.filter()
def concat(value, arg):
    return str(value)+str(arg)

@register.filter()
def define(val=None):
  return val