from django import template
import locale

register = template.Library()

@register.filter
def custom_currency(value, currency_symbol="€"): 
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    formatted_value = locale.format_string('%.2f', value, grouping=True)
    return f"{currency_symbol} {formatted_value}"
