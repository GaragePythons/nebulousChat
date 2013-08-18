def findMessageType(rawInput, keywordTuples, default):
    messageType = 0
    for keywordTuple in keywordTuples:
        messageType += 1
        if type(keywordTuple) is tuple:
	        for keyword in keywordTuple:
	            # print "Checking for keyword " + keyword
	            if(rawInput.startswith('/' + keyword + ' ')):
	                return messageType
    return default

def stripKeyword(rawInput):
	return rawInput.split(' ',1)[1]
