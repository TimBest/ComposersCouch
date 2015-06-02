
def fieldtype(field):
    return field.field.widget.__class__.__name__

AnnoyingGlobals = {
    'fieldtype' : fieldtype,
}
