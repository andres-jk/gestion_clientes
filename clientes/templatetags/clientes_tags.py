# Filtros personalizados para plantillas Django.

from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    # Verifica si el usuario pertenece a un grupo específico
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return user.groups.filter(name=group_name).exists()

@register.filter
def miles_colombianos(value):
    """
    Formatea un número con puntos como separador de miles (estilo colombiano).
    Ejemplo: 1234567 -> 1.234.567
    """
    try:
        value = int(value)
        return '{0:,}'.format(value).replace(',', '.')
    except Exception:
        return value

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)