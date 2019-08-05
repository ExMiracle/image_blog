from django import template

register = template.Library()

@register.simple_tag
def follow_check(me, someone):
    return me.follow_check(someone)