from django import template
register = template.Library()

@register.filter
def verbose_name(value):
    return value._meta.verbose_name


@register.filter
def verbose_name_plural(value):
    return value._meta.verbose_name_plural


@register.filter
def price_with_discount(value, discount):
    return float(value) - ((float(value) / 100) * float(discount))
