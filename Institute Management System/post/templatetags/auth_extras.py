from django import template
from ..models import Liked, Post


register = template.Library()


@register.filter(name='has_liked')
def has_liked(user, post_id):
    post = Post.objects.get(pk=post_id)
    user = Liked.objects.filter(user=user, post=post).first()

    return True if user else False

