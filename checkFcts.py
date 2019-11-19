
of = open("outputLex.txt", 'w')

#Checks to see if a character is a letter
def isLetter(char):
    if(char.isalpha() or char == '$'):
        return True
    return False
#Checks to see if a character is a digit
def isDigit(char):
    if(char.isdigit() or char == '.' or char == '-' or char == '+'):
        return True
    return False

#Checks to see if a character is a space or return character
def isSpace(char):
    if(char == ' ' or char == '\n'):
        return True
    return False

#Checks to see if a character is a separator
def isSeparator(char):
    seps = ['(', ')', '{', '}', ';', ',']

    if(char in seps):
        return True
    return False

#Checks to see if a character is an operator
def isOperator(char):
    ops = ['+', '-', '*', '/', '>', '<', '=', '<=', '>=']

    if (char in ops):
        return True
    return False

#Checks to see if a character is a comment
def isComment(char):
    if (char == '!'):
        return True
    return False

#Checks to see if a character is a keword
def isKeyword(char):
    key = ('int', 'if', 'else', 'real', 'for', 'while', 'whileend', 'then', 'endif', 'do', 'begin', 'end')
    if (char in key):
        return True
    return False


#Checks to see if a lexeme is a keyword or identifier
def endWord(state, lexeme, line):
    if(len(lexeme) > 0):
        if(isKeyword(''.join(lexeme))):
            of.write('{:<15}'.format('KEYWORD'))
            of.write('{:<8}'.format(line))
            of.write(''.join(lexeme) + '\n')
            
##            print('{:<15}'.format('KEYWORD'), end='')
##            print('{:<8}'.format('='),end='')
##            print(''.join(lexeme))
        elif(state == 3 or state == 4 or state == 5):
            of.write('{:<15}'.format('IDENTIFIER'))
            of.write('{:<8}'.format(line))
            of.write(''.join(lexeme) + '\n')
            
##            print('{:<15}'.format('IDENTIFIER'), end='')
##            print('{:<8}'.format('='),end='')
##            print(''.join(lexeme))

#Checks to see if a lexeme is a real or an integer
def endNum(state, lexeme, isReal, line):
    if(len(lexeme) > 0):
##        print (state)
        if(isReal and (state == 3)):
            of.write('{:<15}'.format('REAL'))
            of.write('{:<8}'.format(line))
            of.write(''.join(lexeme) + '\n')
            
##            print('{:<15}'.format('REAL'), end='')
##            print('{:<8}'.format('='),end='')
##            print(''.join(lexeme))
        elif(not(isReal) and (state == 2)):
            of.write('{:<15}'.format('INTEGER'))
            of.write('{:<8}'.format(line))
            of.write(''.join(lexeme) + '\n')
            
##            print('{:<15}'.format('INTEGER'), end='')
##            print('{:<8}'.format('='),end='')
##            print(''.join(lexeme))
        
#Converts the states for an integer to the states for a
#real number if a decimal is detected
def intToReal(lexeme):
    state = 0

    newChar = 0
    
    realGrid = [
    [1,2,4],
    [1,2,4],
    [3,4,4],
    [3,4,4],
    [4,4,4]]
##    print(state)
    for i in lexeme:
        if(i == '-' or i == '+'):
            continue
        if(i.isdigit()):
##            print('number')
            newChar = 0
        elif(i == '.'):
##            print('decimal point')
            newChar = 1
        else:
            newChar = 2
        state = realGrid[state][newChar]
##    print (state)
    
    return state
