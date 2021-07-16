def delOrParseFloat(dictonary, prop):
    if not dictonary[prop]:
        del dictonary[prop]
    else:
        dictonary[prop] = float(dictonary[prop])
