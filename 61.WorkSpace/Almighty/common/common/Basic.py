import re
import logging
import emoji

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

def removeNotUtf8(string):
    blog = logging.getLogger('Batch')
    blog.debug('Call function removeNotUtf8/string : ' + str(string))
    if type(string) == str:
        string = replaceEmoji(string)
        blog.debug(type(string))
        blog.debug("after Remove")
        blog.debug(string)


    return string

# def give_emoji_free_text(text):
#     allchars = [c2 for c2 in text.decode('utf-8')]
#     emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
#     clean_text = ' '.join([c2 for c2 in text.decode('utf-8').split() if not any(i in c2 for i in emoji_list)])
#     return clean_text

def replaceEmoji(inputString):
    string = emoji.replace_emoji(inputString, replace='')
    return string

def tuple2Str(tuple):
    return "%s" % tuple

if __name__ == '__main__':
    s1 = '안녕 🤔 How is your 🙈 and 😌. Have a nice weekend 💕👭👙'
    #s1 = a(s1)
    print(s1)


    #print(s2)