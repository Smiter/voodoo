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
    base_price = float(value)
    additional_price = base_price * (0.5 - float(discount) / 100)
    
    result = base_price + additional_price
    
    return result
