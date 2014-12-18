import datetime

def now(request):
    return {'now':datetime.datetime.now()}
