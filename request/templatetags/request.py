from django.template import Library

register = Library()


@register.simple_tag
def hide_accept(private_request, user):
    accepted = private_request.has_accepted(user)
    if accepted:
        return "hidden"
    return None

@register.simple_tag
def hide_decline(private_request, user):
    accepted = private_request.has_accepted(user)
    if accepted != True:
        return "hidden"
    return None
