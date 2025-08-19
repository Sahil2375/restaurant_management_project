from django import template

register = template.Library()

@register.filter(name='availability')
def availability(item):
    # Returns the item name if available, otherwise returns 'Coming Soon'.
    if hasattr(item, 'is_available') and not item.is_available:
        return f"{item.name} (Coming Soon)"
    return item.name