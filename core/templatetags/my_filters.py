from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.simple_tag()
def currency(v, *args, **kwargs):
    # you would need to do any localization of the result here
    result = round(float(v), 2)
    return (str(result).replace(".", ","))

register.filter('currency', currency)