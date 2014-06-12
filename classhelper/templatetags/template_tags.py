from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter('get_class')
def get_class(ob):
    return ob.__class__.__name__

@register.filter('fix_radio', is_safe=True)
def fix_radio(radio, args):
    radio = str(radio)
    radio = radio.replace('>', 'class="rating-input" id="%s">' % (args))
    return radio

@register.filter('merge', is_safe=True)
def merge(string, integer):
    return string + str(integer)


@register.filter('jsonify', is_safe=True)
def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(simplejson.dumps(object))

@register.filter('dictionary')
def dictionary(dictionary, key):
    try:
        return dictionary[key]
    except KeyError:
        return "-"

@register.inclusion_tag('stars.html')
def stars(value, code, typ):
    stars = None
    if value:
        stars = range(1,value +1)

    return {'value' : value, 'code' : code, 'stars' : stars, 'type' : typ}
