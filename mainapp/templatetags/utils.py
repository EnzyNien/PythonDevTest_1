from django import template
from mainapp.models import Clients

register = template.Library()
field_names = list(Clients.get_field_names_gen())

@register.simple_tag(name='get_fields_from_row')
def get_fields_from_row(row):
    return [getattr(row,item) for item in field_names]
