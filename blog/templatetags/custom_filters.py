from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css_class):
    """Add a CSS class to a form field."""
    if not isinstance(field, BoundField):
        return field
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='addplaceholder')
def addplaceholder(field, placeholder):
    """Add a placeholder to a form field."""
    if not isinstance(field, BoundField):
        return field
    return field.as_widget(attrs={'placeholder': placeholder})
