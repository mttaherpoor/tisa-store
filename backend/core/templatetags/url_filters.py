from django import template

register = template.Library()

@register.filter
def endswith(value: str, suffix: str) -> bool:
    return bool(value) and value.endswith(suffix)
