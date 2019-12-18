import lexer
import sys

NonTerminals = {'S' : 'Statement', 'E':'Expression','D' : 'Declarative', 'C':'Conditional', 'A': 'Assign', 'W':'MoreStatements','V':'MoreIds', 'F' : 'Factor','T':'Term','X':'MoreExpressions','Y':'MoreTerms','Z':'MoreConditionals'}
#Text rules to be printed out when needed
Rules = [
    '''<Statement> -> <Assign> | <Declarative>
       | if <Conditional> then <Statement> else <Statement> endif
       | while <Conditional> do <Statement> whileend
       | begin <Statement> <MoreStatements> end''',
    '''<MoreStatements> -> ; <Statement> <MoreStatements> | <empty>''',
    '''<Conditional> -> <Expression> <MoreConditionals>''',
    '''<MoreConditionals> -> <relop> <Expression | <empty>''',
    '''<Assign> -> <id> = <Expression> <MoreStatements> ;''',
    '''<Expression> -> <Term> <MoreExpressions>''',
    '''<MoreExpressions -> + <Term> <MoreExpressions> | - <Term> <MoreExpressions> | <empty>''',
    '''<Term> -> <Factor> <MoreTerms>''',
    '''<MoreTerms> -> * <Factor> <MoreTerms> | / <Factor> <MoreTerms> | <empty>''',
    '''<Factor> -> ( <Expression> ) | <id> | <num>''',
    '''<Declarative> -> <type> <id> <MoreIds>; | <empty>''',
    '''<MoreIds> -> , <id> <MoreIds> ; | <empty>''']
#rows corresponding to the table
Row = { 'S':0, 'A':1, 'W':2, 'V':3, 'D':4, 'C':5, 'E':6, 'T':7, 'F':8, 'X':9, 'Y':10, 'Z':11}
#rows corresponding to the rules
RowRule = { 'S':0, 'W':1, 'C':2, 'Z':3, 'A':4, 'E':5, 'X':6, 'T':7, 'Y':8, 'F':9, 'D':10, 'V':11}
#column values corresponding to the columns in the table
Col = { '$':0, 'if':1, 'then':2, 'else':3, 'endif':4, 'while':5, 'do':6, 'whileend':7, 'begin':8, 'end':9, ';':10, ',':11, 'id':12, 'num':13, 'type':14, 'relop':15, '(':16, ')':17, '+':18, '-':19, '*':20, '/':21}

#parse table for finding the rules to be added to the stack
ParseTable = [
    ['~', 'if C then S else S endif', '@', '~', '~', 'while C do S whileend', '@', '~', 'begin S W end', '~', '~', '@', 'A', '@', 'D', '@', '@', '@', '@', '@', '@', '@'],#S
    ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', 'id = E W', '@', '@', '@', '@', '@', '@', '@', '@', '@'],#A
    ['@', '@', '@', '~', '~', '@', '@', '@', '@', '~', '; S W', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@'],#W
    ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '~', ', id V', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@'],#V
    ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', 'type id V', '@', '@', '@', '@', '@', '@', '@'],#D
    ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', 'E Z', 'E Z', '@', '@', 'E Z', '@', '@', '@', '@', '@'],#C
    ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', 'T X', 'T X', '@', '@', 'T X', '@', '@', '@', '@', '@'],#E
    ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', 'F Y', 'F Y', '@', '@', 'F Y', '@', '@', '@', '@', '@'],#T
    ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', 'id', 'num', '@', '@', '( E )', '@', '@', '@', '@', '@'],#F
    ['@', '@', '~', '@', '@', '@', '@', '@', '@', '@', '~', '@', '@', '@', '@', '~', '@', '~', '+ T X', '- T X', '@', '@'],#X
    ['@', '@', '~', '@', '@', '@', '@', '@', '@', '@', '~', '@', '@', '@', '@', '~', '@', '~', '~', '~', '* F Y', '/ F Y'],#Y
    ['@', '@', '~', '@', '@', '@', '~', '@', '@', '@', '@', '@', '@', '@', '@', 'relop E', '@', '@', '@', '@', '@', '@']#Z
]

# create symbol table using the output of the lexer
def createTable(tokens, lines, lexemes):
    datatype = ''
    variables = []
    identList = []
    for i in range(len(lines)):
        if tokens[i] == 'KEYWORD':
            datatype = lexemes[i]
        elif tokens[i] == 'IDENTIFIER':
            if not(lexemes[i] in identList):
                variables.append((lexemes[i],datatype))
                identList.append(lexemes[i])

    return variables


# function to help split up the line read in that was created from the lexer
def parseTerms(line):
    words = []
    for a in line.split('\n'):
        if a != '':
            for i in a.split(' '):
                if i != '':
                    words.append(i)
    return words
#Begin Processing
stack = ['$']

#load starting rule
stack.append('S')

#run through the lexer
lexer.lex()

#open up the input file for the syntactical analysis, it uses the output of the lexer
SAinFile = open('outputLex.txt')
#open up an output file for the output of the syntactical analysis
SAoutFile = open('outputSA.txt', mode = 'w')

##print(ParseTable[Row['S']][Col['if']])
for i in SAinFile.readlines()[1:]:
    #header info formatting
    lineInfo = parseTerms(i)
    print('Token: ', end='')
    print('{:<15}'.format(lineInfo[0]), end='')
    print('Lexeme: ' + lineInfo[2])
    SAoutFile.write('Token: ')
    SAoutFile.write('{:<15}'.format(lineInfo[0]))
    SAoutFile.write('Lexeme: ' + lineInfo[2] + '\n')
    #end header info formatting


    #get all tokens, lines, and lexemes
    #print(stack[-1])
    #set parsed data from the lexer to variables
    curData = lineInfo[2]
    curToke = lineInfo[0]

    #will run a loop on the current lexeme until it is a match and will proceed
    ifEqu = True
    while ifEqu:
        # if the value is found then it will be popped off of the stack and the next lexeme will be selected
        if (curData == stack[-1] or((curData == 'int' or curData == 'bool' or curData == 'real') and stack[-1] == 'type') or ((curToke == 'INTEGER' or curToke == 'REAL') and stack[-1] == 'num') or ((curToke == 'IDENTIFIER') and stack[-1] == 'id') or ((curToke == 'OPERATOR') and stack[-1] == 'relop')):
            swap = stack.pop()
            ifEqu = False
            print('\n')
            SAoutFile.write('\n\n')
        # all cases where the top of stack and lexeme do not match       
        else:
##            print(stack)
            #pop the value off of the top of the stack
            swap = stack.pop()

            #check to see if need to change the col name based on the token
            dataCol = ''
            if(curToke == 'INTEGER'or curToke == 'FLOAT'):
                dataCol = 'num'
            elif(curToke == 'IDENTIFIER'):
                dataCol = 'id'
            elif(curToke == 'OPERATOR' and (curData == '<' or curData == '<=' or curData == '==' or curData == '<>' or curData == '>=' or curData == '>' )):
                dataCol = 'relop'
            elif(curData == 'bool' or curData == 'int' or curData == 'float'):
                dataCol = 'type'

            #if the col name was not changed then use the real value
            if dataCol == '':
                dataCol = curData

            #store the rule from the parse table into a variable
            Rule = ParseTable[Row[swap]][Col[dataCol]]
            #split up the different terminals and non terminals into a list
            newRule = Rule.split(' ')
            #reverse the list
            newRule.reverse()
            #check to see if the top of the list is an error value
            if(newRule[0] == '@'):
##                print(stack)
                print("ERROR WITH "+str(dataCol) + " ON LINE " + str(lineInfo[1]))
                SAoutFile.write("ERROR WITH "+str(dataCol) + " ON LINE " + str(lineInfo[1]) + "\n")
                input()
                SAinFile.close()
                SAoutFile.close()
                sys.exit()
            #check to see if the top of the list is an epsilon
            elif(newRule[0] == '~'):
                #ifEqu = 
                print(Rules[RowRule[swap]])
                print('<empty> -> <epsilon>')
                SAoutFile.write(Rules[RowRule[swap]] + '\n')
                SAoutFile.write('<empty> -> <epsilon>' + '\n')
            #if not an error or epsilon then replace the non terminal value and append the new rules
            else:
                for a in newRule:
                    stack.append(a)
                print(Rules[RowRule[swap]])
                SAoutFile.write(Rules[RowRule[swap]] + '\n')
#check to see if the input was parsed successfully
if stack[-1] == '$':
    stack.pop()
    print('Successfully Parsed')
    SAoutFile.write('Successfully Parsed' + '\n')
    # tableInfo = createTable(curToke,curTokeLine,curData)
    # for i in range(tableInfo):
    #     print(i)
else:
    print('Failed to Parse')
    SAoutFile.write('Failed to Parse' + '\n')
SAinFile.close()


varInFile = open('outputLex.txt')

if len(stack) == 0:
    tokens = []
    lines = []
    lexemes = []
    SAoutFile.write('{:<15}'.format('\n\nIdentifier'))
    SAoutFile.write('{:<20}'.format('MemoryLocation'))
    SAoutFile.write('Type' + '\n')
    memLocation = 5000
    print('{:<15}'.format('Identifier'),end='')
    print('{:<20}'.format('MemoryLocation'),end='')
    print('Type')

    for i in varInFile.readlines()[1:]:


        values = parseTerms(i)
        tokens.append(values[0])
        lines.append(values[1])
        lexemes.append(values[2])

    tableInfo = createTable(tokens,lines,lexemes)
    for i in tableInfo:
        print('{:<15}'.format(i[0]), end='')
        print('{:<20}'.format(memLocation), end='')
        print(i[1])

        SAoutFile.write('{:<15}'.format(i[0]))
        SAoutFile.write('{:<20}'.format(memLocation))
        SAoutFile.write(i[1] + '\n')
        memLocation = memLocation + 1

    varInFile.close()



SAoutFile.close()