def splitStringSize(str,size):
    startIndex = 0
    list = []
    while True:
        if len(str) < startIndex + size:
            list.append(str[startIndex:])
            break
        else:
            list.append(str[startIndex:startIndex+size])
            startIndex = startIndex + size
    return list

def tuple2Str(tuple):
    return "%s" % tuple