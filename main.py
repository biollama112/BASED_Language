import os
import sys
import re

EOF = "EOF"
INVALID = "INVALID"

LETTER = 0
DIGIT = 1
UNKNOWN = 99
QUOTE = 2
 
INT_LIT = "Integer"
VAR = "Variable"
CONST = "Constant"
IDENT = "Identifier"
ASSIGN_OP = "Assignment_Operator"
ADD_OP = "Arithmetic_Addition"
SUB_OP = "Arithmetic_Subtraction"
MULT_OP = "Arithmetic_Multiplication"
DIV_OP = "Arithmetic_Division"
LEFT_PAREN = "Left_Parenthesis"
RIGHT_PAREN = "Right_Parenthesis"
LEFT_CURLY = "Left_Curly_Brace"
RIGHT_CURLY = "Right_Curly_Brace"
GREATER_THAN = "Greater_Than"
LESS_THAN = "Less_Than"
TEXT = "Text"
IF_CODE = "If_Statement"
ELSE_CODE = "Else_Statement"
WHILE_CODE = "While_Loop"
FOR_CODE = "For_Loop"
DO_CODE = "Do_Loop"
INT_CODE = "Data-Type_Integer"
FLOAT_CODE = "Data_Type_Float"
STRING_CODE = "Data_Type_String"
SWITCH_CODE = "Switch_Statement"
STRING_LITERAL = "String_Literal"
INPUT_CODE = "Input_Command"
OUTPUT_CODE = "Output_Command"
SEPARATOR = "Separator"
SEMI_COLON = "Semi_Colon"

lexeme = ""
lexLen = 0

def lookupSymbol(character):
    if (character == "("):
        nextToken = LEFT_PAREN
    elif (character == ")"):
        nextToken = RIGHT_PAREN
    elif (character == "+"):
        nextToken = ADD_OP
    elif (character == "-"):
        nextToken = SUB_OP
    elif (character == "*"):
        nextToken = MULT_OP
    elif (character == "/"):
        nextToken = DIV_OP
    elif (character == "="):
        nextToken = ASSIGN_OP
    elif (character == "{"):
        nextToken = LEFT_CURLY
    elif (character == "}"):
        nextToken = RIGHT_CURLY
    elif (character == ">"):
        nextToken = GREATER_THAN
    elif (character == "<"):
        nextToken = LESS_THAN
    elif (character == ","):
        nextToken = SEPARATOR
    elif (character == ';'):
        nextToken = SEMI_COLON
    else:
        nextToken = INVALID
    
    return nextToken


def getChar():
    global inputContent
    global fileIndex
    if (fileIndex < len(inputContent)):
        nextChar = inputContent[fileIndex]
        fileIndex+=1
        return nextChar
    else:
        return EOF
    

def getNonBlank():
    char = getChar()
    while (char.isspace()):
        char = getChar()
    return char

def getCharClass(char):
    if char.isalpha():
        charClass = LETTER
    elif char.isdigit():
        charClass = DIGIT
    elif (char == '"'):
        charClass = QUOTE
    else:
        charClass = UNKNOWN
    return charClass

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def lex(char):
    lexeme = ""
    charClass = getCharClass(char)
    global fileIndex

    if (charClass == LETTER):
        lexeme+=char
        nextChar = getChar()
        while(nextChar != EOF and nextChar != " " and (getCharClass(nextChar) == LETTER or getCharClass(nextChar) == DIGIT)):
            lexeme+=nextChar
            nextChar = getChar()
        
        if (lexeme == "if"):
            nextToken = IF_CODE
        elif (lexeme == "for"):
            nextToken = FOR_CODE
        elif (lexeme == "else"):
            nextToken = ELSE_CODE
        elif (lexeme == "while"):
            nextToken = WHILE_CODE
        elif (lexeme == "do"):
            nextToken = DO_CODE
        elif (lexeme == "int"):
            nextToken = INT_CODE
        elif (lexeme == "float"):
            nextToken = FLOAT_CODE
        elif (lexeme == "string"):
            nextToken = STRING_CODE
        elif (lexeme == "switch"):
            nextToken = SWITCH_CODE
        elif (lexeme == "var"):
            nextToken = VAR
        elif (lexeme == "constant"):
            nextToken = CONST
        elif (lexeme == "basedin"):
            nextToken = INPUT_CODE
        elif (lexeme == "basedout"):
            nextToken = OUTPUT_CODE
        else:
            nextToken = IDENT

        if nextChar != " " and nextChar != EOF:
            fileIndex -= 1

    elif (charClass == DIGIT):
        lexeme+=char
        nextChar = getChar()
        while( (nextChar != EOF) and (nextChar != " ") and (getCharClass(nextChar) == DIGIT) ):
            lexeme+=nextChar
            nextChar = getChar()
        nextToken = INT_LIT
        if nextChar != " " and nextChar != EOF:
            fileIndex -= 1

    elif (charClass == QUOTE):
        lexeme = '"'
        nextChar = getChar()
        lexeme += nextChar
        quote_string = '"'
        while(nextChar != '"'):
            nextChar = inputContent[fileIndex]
            lexeme += nextChar
            fileIndex += 1
        nextToken = STRING_LITERAL
         
        
        
    elif (charClass == UNKNOWN):
        token = lookupSymbol(char)
        lexeme+=char
        nextToken = token
    print (lexeme, "\t\t\t\t", nextToken)
    return nextToken

def Lexical_Error():
    line = []
    count = 0

    try:
        f = open(file = fileName, mode= 'r', encoding = "utf8")
    except NameError:
        print("File Does Not Exist!")
    else:
        print("Lexical Errors:")
    
    with open(file = fileName, mode= 'r') as f:
        list_of_lines = f.readlines()
        line_increment = 0
        total_lexical_errors = 0
        for line in list_of_lines:
            words = line.split()
            for word in words:      
                keywords = ["int", 'float', 'double', 'char', 'string', 'bool', 'if', 'else', 'do', 'while', 'for', 'switch', 'var', 'constant', 'basedin', 'basedout',  '[', ']', '(', ')'
                ,'{', '}', ';', '""', "''", '"', "'", " ", "=", "==", "+", "-", "*", "**", "<", ">", ">>", "<<", ">=", "<=", "&&", "||", "/"]
                error_keywords = ["!", "@", "&", "$", "#", "%", "?", "|"]
                error_word = False
                if word not in keywords or word in error_keywords:
                    for keyword in keywords:
                        if keyword in word:
                            error_word = True
                            break
                    if not error_word:
                        identifier = False
                        for letter in word:
                            if letter.isalpha() == True:
                                identifier = True
                                continue
                            else:
                                identifier = False
                                break
                        if identifier == False:
                            is_float = isfloat(word)
                            is_digit = word.isdigit()
                            if is_digit == True:
                                int_word = int(word)
                                if int_word >= 2047483646:
                                    print("Integer out of bounds", int_word)
                                    print("In line ", line_increment +1)
                                    total_lexical_errors += 1
                                if int_word <= -2047483646:
                                    print("Integer out of bounds", int_word)
                                    print("In line ", line_increment +1)
                                    total_lexical_errors += 1
                                continue
                            elif is_float == True:
                                continue
                            elif is_digit == False:
                                print("Invalid Keyword: " + word)
                                print("In line ", line_increment+1)
                                total_lexical_errors += 1
            line_increment += 1
            if f == EOF:
                break
        if total_lexical_errors == 0:
            print("No errors found! :)")
     
def Syntax_Error():
    open_char = ["(" , "{",  "["]
    closed_char = [")", "}", "]"]
    quote_mark = ['"', "'", "`"]
    stack2 = []
    stack = []
    try:
        f = open(file = fileName, mode= 'r', encoding = "utf8")
    except NameError:
        print("File Does Not Exist!")
    else:
        print("Syntax Errors:")
    
    with open(file = fileName, mode= 'r') as f:
        list_of_lines = f.readlines()
        line_increment = 0
        for line in list_of_lines:
            words = line.split()
            words = line.strip()
            for word in words:
                if word in open_char:
                    stack.append(word)
                elif word in closed_char:
                    if len(stack) > 0:
                        if (word == ")" and stack[-1]== "(" ) or (word == "}" and stack[-1]== "{" ) or (word == "]" and stack[-1]== "["):
                            stack.pop()
                        else:
                            stack.append(word)   
                    else:
                        stack.append(word)
                if word in quote_mark:
                    if stack2 and stack2[-1] == word:
                        stack2.pop()
                    else:
                        stack2.append(word)
                else:
                    pass
                
    if len(stack) == 0:
        print("No Errors!")   
    if len(stack) != 0:
        print("Unmatched usage of parentheses: ",stack)
    elif len(stack2) != 0:
        print("EOL while scanning string literal:" , stack2)


def Semantic_Error():
    line = []
    count = 0
    types = ['int', 'float', 'double', 'char', 'string', 'bool']
    varconst = ['var', 'const']
    try:
        f = open(file = fileName, mode= 'r', encoding = "utf8")
    except NameError:
        print("File Does Not Exist!")
    else:
        code = f.read()
        print("Semantic Errors:")
    
    with open(file = fileName, mode= 'r') as f:
        list_of_lines = f.readlines()
        line_increment = 0
        
    total_semantic_errors = 0
    for line in list_of_lines:
        words = line.split()
        for word in words:

            if words[1] == "int":
                if not re.match("^[-+]?[0-9]+$", words[4]):
                    print("In line", line_increment+1)
                    print("NOT INTEGER >>", line)
                    total_semantic_errors += 1
                    break
                else:
                    pass
                
            elif words[1] == "float":
                if re.match("^[-+]?[0-9]+$", words[4]):
                    print("In line", line_increment+1)
                    print("NOT FLOAT >>", line)
                    total_semantic_errors += 1
                    break
                else:
                    pass
                
            elif words[1] == "double":
                if re.match("^[-+]?[0-9]+$", words[4]):
                    print("In line", line_increment+1)
                    print("NOT DOUBLE >>", line)
                    total_semantic_errors += 1
                    break
                else:
                    pass  

            if words[0] in varconst: 
                if words[1] not in types:
                    print ("In line", line_increment+1)
                    print("Variable not initialized >> ", line)
                    total_semantic_errors += 1
                    break          
                else:
                    pass 
            if word not in types:
                continue              
        line_increment += 1
        if f == EOF:
            break
    if total_semantic_errors == 0:
        print("No semantic errors!")
        
def main(): 
    print ("LEXEMES","\t\t\t", "TOKENS")
    print ("-------","\t\t\t", "------")
    nextChar = getNonBlank()
    if (nextChar == EOF):
        print ("File is empty")
        return

    while nextChar != EOF:
        nextToken = lex(nextChar)
        if (nextToken == INVALID):
            break
        nextChar = getNonBlank()
    
    
    


while True:

    print("==================================")
    print("""
    [1] Upload .txt file
    [2] View Lexemes/Tokens
    [3] View Lexical Errors
    [4] View Syntax Errors
    [5] View Semantic Errors
    [6] Exit Main Menu
    """)
    print("==================================")

    user_input = int(input("Enter a number: "))
    
    if user_input == 1:
        fileName = "input.txt"
        inputFile = open(file=fileName, mode="r", encoding="utf8")
        inputContent = inputFile.read()
        fileIndex=0
        os.system('cls')
        print("File Uploaded!")
        continue

    elif user_input == 2:
        os.system('cls')
        main()
        continue

    elif user_input == 3:
        Lexical_Error()
       
        continue

    elif user_input == 4:
        Syntax_Error()
    
    elif user_input == 5:
        Semantic_Error()
        continue

    elif user_input == 6:
        os.system('cls')
        break

    else: 
        print("Invalid choice. Try again.")
        continue

    
















