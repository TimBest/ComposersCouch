import django
from django import template

from smart_if import smart_if


register = template.Library()

@register.filter
def get_item(dictionary, key):
    """ try to find the item in the dictionary. if it is not found
        convert the key to a string and try again. If nither are found
        retunr None """ 
    try:
        item = dictionary[key]
    except:
        item = dictionary.get(str(key))
    return item


try:
    if int(django.get_version()[-5:]) < 11806:
        register.tag('if', smart_if)
except ValueError:
    pass
