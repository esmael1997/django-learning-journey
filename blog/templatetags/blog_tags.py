from django import template
from blog.models import Post
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('blog/latest_posts.html')
def show_latset_posts(count=8):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:count]
    return {'latest_posts': posts}

