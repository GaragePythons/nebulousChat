def findMessageType(rawInput, keywordTuples, default):
    messageType = 0
    for keywordTuple in keywordTuples:
        if type(keywordTuple) is tuple:
	        for keyword in keywordTuple:
	            # print "Checking for keyword " + keyword
	            if rawInput.startswith('/' + keyword + ' '):
	                return messageType
        messageType += 1
    return default

def stripKeyword(rawInput):
	return rawInput.split(' ',1)[1]
