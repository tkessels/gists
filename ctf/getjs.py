def getjss(text):
    return "String.fromCharCode({})".format(",".join(["{}".format(ord(x)) for x in text]))
