import checkFcts
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def lex():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    #####################################################################
    ###########    RUN THE PROGRAM AND CLICK THE INPUT FILE    ##########
    #####################################################################

    #CAN CHANGE filename TO THE NAME OF AN INPUT FILE IN THE SAME DIRECTORY

    iF = open(filename, 'r')

    lineCounter = 1

    #Flags to be checked and unchecked based on conditions in the program
    inCommentFlag = False
    inWord = False
    inNum = False
    isReal = False


    checkFcts.of.write('{:<17}'.format('TOKENS'))
    checkFcts.of.write('{:<5}'.format(' '))
    checkFcts.of.write('Lexemes\n')
        
    ##print('{:<15}'.format('TOKENS'), end='')
    ##print('{:<7}'.format(' '),end='')
    ##print('Lexemes')

    #Keeps track of the current state of the Finite state machine
    state = 0

    #Holds all of the characters for a single lexeme
    lexeme = []

    #Checks to see if conditions need to be reset
    reset = False

    #DFA for IDENTIFIERS
    identifierGrid = [
        [ 3, 1, 2],
        [ 1, 1, 1],
        [ 2, 2, 2],
        [ 4, 5, 2],
        [ 4, 5, 2],
        [ 4, 5, 2]]

    #DFA for REAL numbers
    realGrid = [
        [1,2,4],
        [1,2,4],
        [3,4,4],
        [3,4,4],
        [4,4,4]]

    #DFA for INTEGER numbers
    integerGrid = [
        [1,1,2,3],
        [3,3,2,3],
        [3,3,2,3],
        [3,3,3,3]]

    #Runs a loop for each line of the input file
    for line in iF:
        #Runs a loop for each character in a line
        for char in line:
            #Gets rid of all comments
            if (checkFcts.isComment(char)):
                if(inCommentFlag == False):
                    inCommentFlag = True
                else:
                    inCommentFlag = False
                inWord = False
                inNum = False
            #Skips the character if it is a comment
            if(inCommentFlag == True):
                continue

            #Spaces or new line characters will trigger this code to check
            # to see if a lexeme needs to be displayed
            if checkFcts.isSpace(char):
                if(inWord):
                    checkFcts.endWord(state, lexeme, lineCounter)
                if(inNum):
                    checkFcts.endNum(state,lexeme, isReal, lineCounter)
                inWord = False
                inNum = False
                reset = True
                #lexeme.append(char)
            #elif():


            #SEPARATORS
            #Checks to see if a character is a separator, if it is then it
            # checks to see if a lexeme needs to be displayed first, then
            # it will display the separator
            elif(checkFcts.isSeparator(char)):
                if(inWord):
                    checkFcts.endWord(state, lexeme, lineCounter)
                if(inNum):
                    checkFcts.endNum(state,lexeme, isReal, lineCounter)
                inWord = False
                inNum = False
                checkFcts.of.write('{:<15}'.format('SEPARATOR'))
                checkFcts.of.write('{:<8}'.format(lineCounter))
                checkFcts.of.write(char + '\n')

    ##            print('{:<15}'.format('SEPARATOR'), end='')
    ##            print('{:<8}'.format('='),end='')
    ##            print(char)
                reset = True
            #OPERATORS
            #Checks to see if a character is a separator, if it is then it
            # checks to see if a lexeme needs to be displayed first, then
            # it will display the operator
            elif(checkFcts.isOperator(char)):
                if(inWord):
                    checkFcts.endWord(state, lexeme, lineCounter)
                if(inNum):
                    checkFcts.endNum(state,lexeme, isReal, lineCounter)
                inWord = False
                inNum = False
                checkFcts.of.write('{:<15}'.format('OPERATOR'))
                checkFcts.of.write('{:<8}'.format(lineCounter))
                checkFcts.of.write(char + '\n')

    ##            print('{:<15}'.format('OPERATOR'), end='')
    ##            print('{:<8}'.format('='),end='')
    ##            print(char)
                reset = True
                
            #If the character is a letter then it starts a section
            # which will create a word and checks the finite state
            # machine to see if it will be a returning state for an
            # identifier
            elif(checkFcts.isLetter(char) or inWord):
                if (not(inWord)):
                    inWord = True
                #IDENTIFIER
                newChar = 0
                if(checkFcts.isDigit(char)):
                    newChar = 1
                elif(checkFcts.isLetter(char)):
                    newChar = 0
                else:#dead state
                    newChar = 2
                state = identifierGrid[state][newChar]
                lexeme.append(char)

            #If the character is a digit then it starts a section
            # which will create a word and checks the finite state
            # machine to see if it will be a returning state for an
            # integer or real number
            elif(checkFcts.isDigit(char) or inNum):
                inNum = True
                newChar = 0
                if(not(isReal)):
                    if(char.isdigit()):
                        newChar = 2
                    elif(char == '+'):
                        newChar = 0
                    elif(char == '-'):
                        newChar = 1
                    elif(char == '.'):
                         isReal = True
                         lexeme.append(char)
                         state = checkFcts.intToReal(lexeme)
                    else:
                        newChar = 3
                    if(not(isReal)):
                        state = integerGrid[state][newChar]
                elif(isReal):
                    if(char.isdigit()):
                        newChar = 0
                    elif(char == '.'):
                        newChar = 1
                    else:
                        newChar = 2
                    state = realGrid[state][newChar]
                if(char != '.'):
                    lexeme.append(char)
            if (reset):
                reset = False
                state = 0
                lexeme = []
        lineCounter = lineCounter + 1
    #makes one final check at the end of the program to see if it will need to
    # output one last lexeme
    if(inWord):
        checkFcts.endWord(state, lexeme, lineCounter)
    if(inNum):
        checkFcts.endNum(state,lexeme, isReal, lineCounter)
    inWord = False
    inNum = False

    checkFcts.of.close()
