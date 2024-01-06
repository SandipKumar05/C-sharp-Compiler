# Reference used - http://manual.freeshell.org/ply/ply.html
# Newer http://www.dabeaz.com/ply/ply.html

import ply.lex as lex
from ply.lex import TOKEN
from sys import argv

identifiers_list = []

tok_table = {
    "BOOL": 0,
    "BREAK": 0,
    "BYTE": 0,
    "CASE": 0,
    "CHAR": 0,
    "CLASS": 0,
    "CONST": 0,
    "CONTINUE": 0,
    "DO": 0,
    "DOUBLE": 0,
    "ELSE": 0,
    "FALSE": 0,
    "FLOAT": 0,
    "FOR": 0,
    "IF": 0,
    "INT": 0,
    "LONG": 0,
    "NAMESPACE": 0,
    "NEW": 0,
    "NULL": 0,
    "OBJECT": 0,
    "OPERATOR": 0,
    "PARAMS": 0,
    "PRIVATE": 0,
    "PROTECTED": 0,
    "PUBLIC": 0,
    "RETURN": 0,
    "STRING": 0,
    "SWITCH": 0,
    "TRUE": 0,
    "UINT": 0,
    "ULONG": 0,
    "USHORT": 0,
    "USING": 0,
    "VOID": 0,
    "WHILE": 0,
    "MULTIPLICATION": 0,
    "DIVISION": 0,
    "MODULUS": 0,
    "ADDITION": 0,
    "SUBTRACTION": 0,
    "LEFTSHIFT": 0,
    "RIGHTSHIFT": 0,
    "LESSTHAN": 0,
    "GREATERTHAN": 0,
    "LESSTHANEQUAL": 0,
    "GREATERTHANEQUAL": 0,
    "EQUALITY": 0,
    "NOTEQUAL": 0,
    "BITAND": 0,
    "BITXOR": 0,
    "BITOR": 0,
    "BITNOT": 0,
    "BITCOMPLEMENT": 0,
    "LOGICALAND": 0,
    "LOGICALOR": 0,
    "NULLCOALESCING": 0,
    "CONDITIONALOPERATOR": 0,
    "ASSIGN": 0,
    "PLUSEQUAL": 0,
    "MINUSEQUAL": 0,
    "MULTIPLYEQUAL": 0,
    "DIVIDEEQUAL": 0,
    "MODULUSEQUAL": 0,
    "ANDEQUAL": 0,
    "OREQUAL": 0,
    "XOREQUAL": 0,
    "LEFTSHIFTEQUAL": 0,
    "RIGHTSHIFTEQUAL": 0,
    "LAMBDA": 0,
    "INCREMENT": 0,
    "DECREMENT": 0,
    "ARROW": 0,
    "BLOCKBEGIN": 0,
    "BLOCKEND": 0,
    "OPENSQUAREBRACKET": 0,
    "CLOSESQUAREBRACKET": 0,
    "OPENPARENTHESIS": 0,
    "CLOSEPARENTHESIS": 0,
    "DOT": 0,
    "COMMA": 0,
    "SEMICOLON": 0,
    "COLON": 0,
    "SCOPERESOLUTIONOPERATOR": 0,
    "SIGNEDINTEGER": 0,
    "UNSIGNEDINTEGER": 0,
    "LONGINTEGER": 0,
    "UNSIGNEDLONGINTEGER": 0,
    "FLOATREAL": 0,
    "DOUBLEREAL": 0,
    "DECIMALREAL": 0,
    "CHARACTER": 0,
    "REGULARSTRING": 0,
    "HEXADECIMALDIGIT": 0,
    "VERBATIMSTRING": 0,
    "IDENTIFIER": 0,
    "COMMENT": 0,
}


operators = [
    "MULTIPLICATION",
    "DIVISION",
    "MODULUS",
    "ADDITION",
    "SUBTRACTION",
    "LEFTSHIFT",
    "RIGHTSHIFT",
    "LESSTHAN",
    "GREATERTHAN",
    "LESSTHANEQUAL",
    "GREATERTHANEQUAL",
    "EQUALITY",
    "NOTEQUAL",
    "BITAND",
    "BITXOR",
    "BITOR",
    "BITNOT",
    "BITCOMPLEMENT",
    "LOGICALAND",
    "LOGICALOR",
    "NULLCOALESCING",
    "CONDITIONALOPERATOR",
    "ASSIGN",
    "PLUSEQUAL",
    "MINUSEQUAL",
    "MULTIPLYEQUAL",
    "DIVIDEEQUAL",
    "MODULUSEQUAL",
    "ANDEQUAL",
    "OREQUAL",
    "XOREQUAL",
    "LEFTSHIFTEQUAL",
    "RIGHTSHIFTEQUAL",
    "LAMBDA",
    "INCREMENT",
    "DECREMENT",
    "ARROW",
]

punctuators = [
    "BLOCKBEGIN",
    "BLOCKEND",
    "OPENSQUAREBRACKET",
    "CLOSESQUAREBRACKET",
    "OPENPARENTHESIS",
    "CLOSEPARENTHESIS",
    "DOT",
    "COMMA",
    "SEMICOLON",
    "COLON",
    "SCOPERESOLUTIONOPERATOR",
]

unicode_escape_sequence = ["HEXADECIMALDIGIT"]

reserved_keywords = [
    "ABSTRACT",
    "AS",
    "BASE",
    "BOOL",
    "BREAK",
    "BYTE",
    "CASE",
    "CATCH",
    "CHAR",
    "CHECKED",
    "CLASS",
    "CONST",
    "CONTINUE",
    "DECIMAL",
    "DEFAULT",
    "DELEGATE",
    "DO",
    "DOUBLE",
    "ELSE",
    "ENUM",
    "EVENT",
    "EXPLICIT",
    "EXTERN",
    "FALSE",
    "FINALLY",
    "FIXED",
    "FLOAT",
    "FOR",
    "FOREACH",
    "GOTO",
    "IF",
    "IMPLICIT",
    "IN",
    "INT",
    "INTERFACE",
    "INTERNAL",
    "IS",
    "LOCK",
    "LONG",
    "NAMESPACE",
    "NEW",
    "NULL",
    "OBJECT",
    "OPERATOR",
    "OUT",
    "OVERRIDE",
    "PARAMS",
    "PRIVATE",
    "PROTECTED",
    "PUBLIC",
    "READONLY",
    "REF",
    "RETURN",
    "SBYTE",
    "SEALED",
    "SHORT",
    "SIZEOF",
    "STACKALLOC",
    "STATIC",
    "STRING",
    "STRUCT",
    "SWITCH",
    "THIS",
    "THROW",
    "TRUE",
    "TRY",
    "TYPEOF",
    "UINT",
    "ULONG",
    "UNCHECKED",
    "UNSAFE",
    "USHORT",
    "USING",
    "VIRTUAL",
    "VOID",
    "VOLATILE",
    "WHILE",
    "CONSOLE",
    "READLINE",
    "WRITELINE",
]

identifiers = ["IDENTIFIER"]

literal_constants = [
    "SIGNEDINTEGER",
    "UNSIGNEDINTEGER",
    "LONGINTEGER",
    "UNSIGNEDLONGINTEGER",
    "FLOATREAL",
    "DOUBLEREAL",
    "DECIMALREAL",
    "CHARACTER",
    "REGULARSTRING",
    "VERBATIMSTRING",
]

comments = ["COMMENT"]

tokens = (
    comments
    + literal_constants
    + reserved_keywords
    + operators
    + identifiers
    + punctuators
    + unicode_escape_sequence
)


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")
    # t.lexer.lineno += len(t.value)
    # t.lineno += t.value.count("\n")
    # print "value hai", str(t.value.count("\n"))


t_ignore = " \t"

t_LEFTSHIFTEQUAL = r"<<="
t_RIGHTSHIFTEQUAL = r">>="
t_LEFTSHIFT = r"<<"
t_RIGHTSHIFT = r">>"

t_LESSTHANEQUAL = r"<="
t_GREATERTHANEQUAL = r">="

t_LESSTHAN = r"<"
t_GREATERTHAN = r">"

t_EQUALITY = r"=="
t_LAMBDA = r"=>"
t_NOTEQUAL = r"!="

t_PLUSEQUAL = r"\+="
t_MINUSEQUAL = r"-="
t_MULTIPLYEQUAL = r"\*="
t_DIVIDEEQUAL = r"/="
t_MODULUSEQUAL = r"%="
t_ANDEQUAL = r"&="
t_OREQUAL = r"\|="
t_XOREQUAL = r"\^="

t_INCREMENT = r"\+\+"
t_DECREMENT = r"--"

t_ARROW = r"->"

t_MULTIPLICATION = r"\*"
t_DIVISION = r"/"
t_MODULUS = r"%"
t_ADDITION = r"\+"
t_SUBTRACTION = r"-"

t_LOGICALAND = r"&&"
t_LOGICALOR = r"\|\|"
t_BITAND = r"&"
t_BITOR = r"\|"
t_BITXOR = r"\^"
# t_BITOR =
t_BITNOT = r"!"
t_BITCOMPLEMENT = r"~"

t_NULLCOALESCING = r"\?\?"
t_CONDITIONALOPERATOR = r"\?"
t_ASSIGN = r"="

t_HEXADECIMALDIGIT = r"\\u[0-9a-fA-F]+"


t_BLOCKBEGIN = r"{"
t_BLOCKEND = r"}"
t_OPENSQUAREBRACKET = r"\["
t_CLOSESQUAREBRACKET = r"\]"
t_OPENPARENTHESIS = r"\("
t_CLOSEPARENTHESIS = r"\)"
t_DOT = r"\."
t_COMMA = r","
t_SEMICOLON = r";"
t_SCOPERESOLUTIONOPERATOR = r"::"
t_COLON = r":"


# literals = ['SIGNEDINTEGER', 'UNSIGNEDINTEGER', 'LONGINTEGER', 'UNSIGNEDLONGINTEGER',
# 'FLOATREAL', 'DOUBLEREAL', 'DECIMALREAL', 'CHARACTER', 'REGULARSTRING', 'VERBATIMSTRING']
reserved_map = {}
for v in reserved_keywords:
    reserved_map[v.lower()] = v


def t_IDENTIFIER(t):
    r"@?[A-Za-z_][\w_]*"
    tok_table["IDENTIFIER"] = tok_table["IDENTIFIER"] + 1
    identifiers_list.append(t.value + ",")
    t.type = reserved_map.get(t.value, "IDENTIFIER")
    return t


# Real constants

floatreal = (
    r"\d*"
    + r"\."
    + r"([0-9]+)"
    + r"([eE][+-]?\d+)"
    + r"?"
    + r"([fF])"
    + r"?"
    + r"|"
    + r"([0-9]+)"
    + r"([eE][+-]?\d+)"
    + r"([fF])"
    + r"?"
    + r"|"
    + r"([0-9]+)"
    + r"([fF])"
)


@TOKEN(floatreal)
def t_FLOATREAL(t):
    t.type = "FLOATREAL"
    return t


doublereal = (
    r"\d*"
    + r"\."
    + r"([0-9]+)"
    + r"([eE][+-]?\d+)"
    + r"?"
    + r"([dD])"
    + r"?"
    + r"|"
    + r"([0-9]+)"
    + r"([eE][+-]?\d+)"
    + r"([dD])"
    + r"?"
    + r"|"
    + r"([0-9]+)"
    + r"([dD])"
)


@TOKEN(doublereal)
def t_DOUBLEREAL(t):
    t.type = "DOUBLEREAL"
    return t


decimalreal = (
    r"\d*"
    + r"\."
    + r"([0-9]+)"
    + r"([eE][+-]?\d+)"
    + r"?"
    + r"([mM])"
    + r"?"
    + r"|"
    + r"([0-9]+)"
    + r"([eE][+-]?\d+)"
    + r"([mM])"
    + r"?"
    + r"|"
    + r"([0-9]+)"
    + r"([mM])"
)


@TOKEN(decimalreal)
def t_DECIMALREAL(t):
    t.type = "DECIMALREAL"
    return t


# Integer constants
unsignedlonginteger = r"0[Xx][0-9a-fA-F]+" + r"|" + r"\d+" + r"[uU][lL]|[lL][uU]"
unsignedinteger = r"0[Xx][0-9a-fA-F]+" + r"|" + r"\d+" + r"[Uu]"
longinteger = r"0[Xx][0-9a-fA-F]+" + r"|" + r"\d+" + r"[Ll]"
signedinteger = r"0[Xx][0-9a-fA-F]+" + r"|" + r"\d+"


@TOKEN(unsignedlonginteger)
def t_UNSIGNEDLONGINTEGER(t):
    t.type = "UNSIGNEDLONGINTEGER"
    return t


@TOKEN(longinteger)
def t_LONGINTEGER(t):
    t.type = "LONGINTEGER"
    return t


@TOKEN(unsignedinteger)
def t_UNSIGNEDINTEGER(t):
    t.type = "UNSIGNEDINTEGER"
    return t


@TOKEN(signedinteger)
def t_SIGNEDINTEGER(t):
    t.type = "SIGNEDINTEGER"
    return t


# Character literals

character_regex = (
    r"[^\'\\\n]"
    + r"|"
    + r"\\[\'\"\\0abfnrtv]"
    + r"|"
    + r"\\x"
    + r"[0-9a-fA-F]"
    + 3 * r"[0-9a-fA-F]?"
    + r"|"
    + r"\\u"
    + 4 * r"[0-9a-fA-F]"
    + r"|"
    + r"\\u"
    + 8 * r"[0-9a-fA-F]"
)
character = r"\'(" + character_regex + r")\'"


@TOKEN(character)
def t_CHARACTER(t):
    t.type = "CHARACTER"
    return t


# String Literals

regular_string = (
    r"\""
    + r"("
    + r"[^\"\\\n]"
    + r"|"
    + r"\\[\'\"\\0abfnrtv]"
    + r"|"
    + r"\\x"
    + r"[0-9a-fA-F]"
    + 3 * r"[0-9a-fA-F]?"
    + r"|"
    + r"\\u"
    + 4 * r"[0-9a-fA-F]"
    + r"|"
    + r"\\u"
    + 8 * r"[0-9a-fA-F]"
    + r")"
    + r"*"
    + '"'
)
verbatim_string = r"@\"" + r"([^\"]|[\"][\"])*" + '"'


# sconst = regular_string_literal + r'|' + verbatim_string_literal
@TOKEN(regular_string)
def t_REGULARSTRING(t):
    t.type = "REGULARSTRING"
    t.lexer.lineno += t.value.count("\n")
    return t


@TOKEN(verbatim_string)
def t_VERBATIMSTRING(t):
    t.type = "VERBATIMSTRING"
    t.lexer.lineno += t.value.count("\n")
    return t


comment = r"/\*(.|\n)*?\*/" + r"|" + r"//(.)*"


@TOKEN(comment)
def t_COMMENT(t):
    t.lexer.lineno += t.value.count("\n")
    print(t.value, " -> COMMENT")
    # t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character %s" % repr(t.value[0])),
    print("line number : %s" % t.lexer.lineno)
    t.lexer.skip(1)


lexer = lex.lex()


def run(test_file):
    code = open(test_file).read()
    with open(test_file) as f:
        for i, j in enumerate(f):
            pass
    length = i + 1
    lexer.input(code)
    token = lexer.token()
    token_line = -1
    if token:
        token_line = token.lineno
    else:
        token_line = -1
    with open(test_file) as f:
        for i, j in enumerate(f):
            if i + 1 == token_line:
                print(token.value, "->", token.type)
                if "IDENTIFIER" not in token.type:
                    tok_table[token.type] = tok_table[token.type] + 1
                token = lexer.token()
                if token:
                    token_line = token.lineno
                else:
                    token_line = -1
                while token_line == i + 1:
                    print(token.value, "->", token.type)
                    if "IDENTIFIER" not in token.type:
                        tok_table[token.type] = tok_table[token.type] + 1
                    token = lexer.token()
                    if token:
                        token_line = token.lineno
                    else:
                        token_line = -1

            print("")


if __name__ == "__main__":
    test_file = argv[1]
    run(test_file)
    for key, value in tok_table.iteritems():
        if value > 0:
            print(key, value)
            if key == "IDENTIFIER":
                print("Identifier list is ", identifiers_list)
