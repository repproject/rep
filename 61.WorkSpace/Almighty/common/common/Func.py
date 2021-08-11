def isNotNull(instance):
    if instance == None:
        return False
    elif len(instance) == 0:
        return False
    return True

def isNull(instance):
    if instance == None:
        return True
    elif len(instance) == 0:
        return True
    return False