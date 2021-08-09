def isValid(obj):
    if obj == None:
        return False
    elif len(obj) == 0:
        return False
    return True

def isNull(obj):
    if obj == None:
        return True
    elif len(obj) == 0:
        return True
    return False