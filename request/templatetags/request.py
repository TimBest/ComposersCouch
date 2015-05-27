

def hide_accept(private_request, user):
    accepted = private_request.has_accepted(user)
    if accepted:
        return "hidden"
    return None

def hide_decline(private_request, user):
    accepted = private_request.has_accepted(user)
    if accepted != True:
        return "hidden"
    return None

RequestGlobals = {
    'hide_accept': hide_accept,
    'hide_decline': hide_decline,
}
