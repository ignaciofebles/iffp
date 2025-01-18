from django import template

register = template.Library()

@register.filter
def custom_currency(value):
    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')  # Configura la localización a español de España
    return locale.format_string('%.2f', value, grouping=True)