"""
	Name: Ngari Kelvin Gauki.
	Reg No: P15/30614/2015.
"""
# function nextchar
def nextChar():
	global inputFile
	return inputFile.read(1)


def decrementFilePtr(offset=-1):
	global inputFile
	inputFile.seek(offset, 1)

# function to match spaces either newline tab or blank space
def matchSpaces(char):
	spaces = ['\n', '\t', ' ', '\r']
	if char not in spaces:
		return False 
	else:
		result = matchSpaces(nextChar())
		if result is False:
			decrementFilePtr()
		return True
# the function  to match comments.

def matchComments(char):
	if '/' in char:
		c = nextChar()
		# Match single line comments
		if '/' in c:
			# Read everything until newline
			while nextChar() != '\n':
				pass
			decrementFilePtr()
			return True

		# Match multiline comments
		elif '*' in c:
			# Keep looping through chars looking for '*/' sequence
			while True:	
				while nextChar() != '*':
					pass
				if '/' in nextChar():
					return True
		else:
			# Not a comment ('/[anything else]')
			return False
	else:
		return False

# the function to for the keywords
def matchKeywords(char):
	# print("key word are like this ")
	# the Array keywords holds the keywords eg include, int
	keywords = ["include", "int", "main", "char", "printf", "getchar", "return"]

	if char in keywords:
		return "<" + char.upper() + ">"
	else:
		string = char
		# Literal
		if "\"" in char or '\'' in char:
			return False

		# Test if string is keyword or identifier
		while string not in keywords:
			c = nextChar()
			# Keep building longest possible string as long as you're reading valid chars
			if c.isalpha() or c.isdigit() or c == '_':
				string += c
				continue
			else:
				# This string is definitely not in keywords
				if c != '':
					# Decr file ptr to initial char
					decrementFilePtr(0 - len(string))
				return False
		return "<" + string.upper() + ">"

		
def matchIdentifiers(char):
	# print("the identifiers are:")
	# Read longest possible string
	string = char
	c = nextChar()
	while c.isdigit() or c.isalpha() or c == '_':
		string += c
		c = nextChar()
	# Reached an invalid char
	if c != '':
		decrementFilePtr()
	# Lookup string
	index = lookup(string)
	if index == -1:
		index = insert(string)
	return "<" + "ID, " + str(index) + ">"


def lookup(string):
	global lexemesArray
	return lexemesArray.index(string) if string in lexemesArray else -1


def insert(string):
	global lexemesArray
	lexemesArray.append(string)
	return (len(lexemesArray) - 1)


def matchDigits(char):
	# print("the digits")
	validItems = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']

	if char not in validItems:
		return False
	else:
		string = char
		c = nextChar()
		while c in validItems:
			string += c
			c = nextChar()

		if c != '':
			decrementFilePtr()
		return "<" + "NUM, " + string + ">"


def matchLiterals(char):
	# Single quoted strings
	if '\'' in char:
		string = char
		# Read everything until next \'
		c = nextChar()
		while c != '\'':
			string += c
			c = nextChar()
		string += '\''
		return "<STRING, " + string + ">"

	# Double quoted strings
	if '\"' in char:
		string = char
		# Read everything until next \"
		c = nextChar()
		while c != '\"':
			string += c
			c = nextChar()
		string += '\"'
		return "<STRING, " + string + ">"

	# Header Files
	decrementFilePtr(-2)
	prevChar = nextChar()
	if "<" in prevChar:
		# Read everything until >
		currChar = nextChar()
		string = currChar
		c = nextChar()
		while c != ">":
			string += c
			c = nextChar()
		if c != '':
			decrementFilePtr()
		return "<STRING, " + "\"" + string + "\"" + ">"
	else:
		# Return file ptr to right position if fail
		decrementFilePtr(1)
	return False


def matchOperators(char):
	operators = {
		"#": "OP_HASH",
		"{": "OP_OP_CURL",
		"}": "OP_CL_CURL",
		"(": "OP_OP_PAR",
		")": "OP_CL_PAR",
		"<": "OP_LESS",
		">": "OP_GREATER",
		"=": "OP_ASSIGN",
		";": "OP_SEMI",
		"+": "OP_ADD",
		"*": "OP_MULT",
		"/": "OP_DIV",
		",": "OP_COMMA"
	}

	if char in operators:
		return "<" + operators[char] + ">"
	else: return False


if __name__ == "__main__":
	inputFile = open("lexical.c", "r")
	outputFile = open("output.txt", "w")
	lexemesArray = []

	while True:
		char = nextChar()
		if char == '':
			# Reached EOF
			break

		if matchSpaces(char):
			continue
		if matchComments(char):
			continue
		else:
			token =  matchOperators(char) or matchDigits(char) or matchKeywords(char) or matchLiterals(char) or matchIdentifiers(char)
			outputFile.write(token)
			print token,
			print("\n")
