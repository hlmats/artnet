from django import template
from ..models import Image

register = template.Library()

@register.inclusion_tag('images/image/latest_paintings.html')
def show_latest_paintings(count=5):
    latest_paintings = Image.objects.filter(activity='Active')[:count]
    return {'latest_paintings': latest_paintings}

@register.inclusion_tag('images/image/most_liked_paintings.html')
def show_most_liked_paintings(count=5):
    most_liked_paintings = Image.objects.filter(activity='Active').order_by('-total_likes')[:count]
    return {'most_liked_paintings': most_liked_paintings}
