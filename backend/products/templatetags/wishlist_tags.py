from django import template

register = template.Library()

@register.filter
def in_wishlist(product, user):
    if not user.is_authenticated:
        return False
    return user.wishlist.filter(product=product).exists()
