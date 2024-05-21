from django import template
from my_app.models import Category

register = template.Library()


@register.simple_tag()
def get_all_categories():
    return Category.objects.all()
