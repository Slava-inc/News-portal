from django import template


register = template.Library()


@register.filter()
def censor(value):
    if type(value) == str:
        return value.replace('редиска', 'р.....!').replace('октагон', 'о....!')
    return value
