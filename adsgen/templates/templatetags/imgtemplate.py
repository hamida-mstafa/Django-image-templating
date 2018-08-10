from django import template

register = template.Library()

@register.filter(name='create')
def cut(*args.,**kwargs):
    print(*args.,**kwargs)
    return value.replace(arg, '')
