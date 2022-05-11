from django import template

register = template.Library()
censorwords = ["дом", "гном", "домик", "гомик", "ххх", "порнхаб"]

@register.filter(name='censor')
def censor(value):
    for a in censorwords:
        b = str(a + ",")
        с = str(b.title())
        value = value.replace(a, "&#129324;")
        value = value.replace(b, "&#129324;")
        value = value.replace(с, "&#129324;")
    return value

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
