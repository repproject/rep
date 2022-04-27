def isNotNull(instance):
    if instance == None:
        return False

    if len(instance) == 0:
        return False
    return True

def isNull(instance):
    try:
        if instance == None:
            return True
        elif len(instance) == 0:
            return True
        return False
    except TypeError:
        return False

def StrReplace(str,delimiter,chgdelimiter=''):
    return str.replace(delimiter,chgdelimiter)