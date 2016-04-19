# import re
# import os
# import sys
# import ply.lex as lex
# import subprocess
import ply.yacc as yacc
import lexer
from sys import argv
import symbolTable as SymbolTable
from tac import *

ST = SymbolTable.SymbolTable()
TAC = ThreeAddressCode()

tokens = lexer.tokens
lexer = lexer.lexer
precedence = (
	('left', 'ADDITION', 'SUBTRACTION', 'CLOSEPARENTHESIS',),
	('left', 'MULTIPLICATION', 'DIVISION'),
	('right','ELSE')
)
# list of level statment for goto part (jump use)
level = {}
counter = 0
def debug(msg):
	global counter
	if counter == 0: 
		print "In program "+ argv[1]
		print msg
		counter = counter + 1
	else:
		print msg
	# raise SyntaxError

def p_compilation_unit(p):
	''' compilation_unit : namespace-member-declaration'''
	p[0] = {}
	# ST.printSymbolTable()
	# TAC.emit('','','','exit')
	
def p_namespace_member_declaration(p):
	''' namespace-member-declaration : NAMESPACE IDENTIFIER namespace-body'''
	p[0] = {}
	
def p_namespace_body(p):
	''' namespace-body : BLOCKBEGIN class-declaration BLOCKEND '''
	p[0] = {}
	
def p_class_declaration(p):
	''' class-declaration : CLASS IDENTIFIER class-body'''
	p[0] = {}

def p_class_body(p):
	''' class-body : BLOCKBEGIN class-member-declarations BLOCKEND'''
	

def p_class_member_declarations(p):
	''' class-member-declarations : class-member-declaration
								  | class-member-declaration class-member-declarations'''
	p[0] = {}
								
def p_class_member_declaration(p):
	'''class-member-declaration : constant-declaration
								| field-declaration
								| method-declaration
								'''
	p[0] = p[1]	

def p_constant_declaration(p):
	''' constant-declaration :  CONST type constant-declarators SEMICOLON
			 '''
	
def p_constant_declarators(p):
	''' constant-declarators : constant-declarator
							 | constant-declarators COMMA constant-declarator
			 '''
	if len(p) == 2:
		p[0] = [p[1]]
	elif len(p) == 4:
		p[0] = p[1] + [p[3]]
	
def p_constant_declarator(p):
	''' constant-declarator : IDENTIFIER ASSIGN constant-expression
			 '''
	p[0] = { 'identifier_name' : p[1], 'place' : p[3]['place']}

def p_constant_expression(p):
	''' constant-expression : expression '''
	p[0] = p[1]

def p_expression(p):
	''' expression : conditional-expression
				   | assignment
			 '''
	p[0] = p[1]
	
def p_conditional_expression(p):
	''' conditional-expression : conditional-or-expression
							   | conditional-or-expression CONDITIONALOPERATOR expression COLON expression
			 '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
			else:
				p[0]['initializer'] = 1
		else:
			debug("type error in or-expression at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
	
def p_conditional_or_expression(p):
	''' conditional-or-expression : conditional-and-expression
								  | conditional-or-expression LOGICALOR conditional-and-expression
			 '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug ("type error in and-expression at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
	
def p_conditional_and_expression(p):
	''' conditional-and-expression : inclusive-or-expression
								   | conditional-and-expression LOGICALAND inclusive-or-expression
			 '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug( "type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])

def p_inclusive_or_expression(p):
	''' inclusive-or-expression : exclusive-or-expression
								| inclusive-or-expression BITOR exclusive-or-expression
			 '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug("type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
	
def p_exclusive_or_expression(p):
	''' exclusive-or-expression : and-expression
								| exclusive-or-expression BITXOR and-expression
			 '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug("type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
	
def p_and_expression(p):
	''' and-expression : equality-expression
					   | and-expression BITAND equality-expression
			 '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug("type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
	
def p_equality_expression(p):
	''' equality-expression : relational-expression
							| equality-expression EQUALITY relational-expression
							| equality-expression NOTEQUAL relational-expression
			 '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug("type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])

	
def p_relational_expression(p):
	''' relational-expression : shift-expression
							  | relational-expression LESSTHAN shift-expression
							  | relational-expression GREATERTHAN shift-expression
							  | relational-expression LESSTHANEQUAL shift-expression
							  | relational-expression GREATERTHANEQUAL shift-expression
							  '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug("type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
	
def p_shift_expression(p):
	''' shift-expression : additive-expression
						 | shift-expression LEFTSHIFT additive-expression
						 | shift-expression RIGHTSHIFT additive-expression
						 '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug("type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
	
def p_additive_expression(p):
	''' additive-expression : multiplicative-expression
							| additive-expression ADDITION multiplicative-expression
							| additive-expression SUBTRACTION multiplicative-expression
							'''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'

			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug("type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
		
	
def p_multiplicative_expression(p):
	''' multiplicative-expression : unary-expression
								  | multiplicative-expression MULTIPLICATION unary-expression
								  | multiplicative-expression DIVISION unary-expression
								  | multiplicative-expression MODULUS unary-expression
								  '''
	p[0] = {}
	# p[0] = p[1]
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0]['place'] = ST.newTemp()
		p[0]['initializer'] = 1
		if p[1]['type'] and p[3]['type'] in ('int','float'):
			p[0]['type'] = 'int'
			if p[1]['initializer'] == 0 or p[3]['initializer'] == 0:
				p[0]['initializer'] = 0 
				debug("identifier not initialize in expression at line no "+str(p.lexer.lineno ))
		else:
			debug("type error  at line no "+str(p.lexer.lineno))
			p[0]['type'] = "none"
		TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
		ST.addIdentifier(p[0]['place'],p[0]['type'])
	
def p_unary_expression(p):
	''' unary-expression :         primary-expression
			 |         ADDITION unary-expression
			 |         SUBTRACTION unary-expression
			 |         BITNOT unary-expression
			 |         BITCOMPLEMENT unary-expression
			 |         MULTIPLICATION unary-expression
			 |         pre-increment-expression
			 |         pre-decrement-expression
			 '''
	p[0] = p[1]
	
def p_primary_expression(p):
	''' primary-expression : array-creation-expression
			 |         primary-no-array-creation-expression
			 '''
	p[0]=p[1]

def p_array_creation_expression(p):
	''' array-creation-expression : NEW simple-type OPENSQUAREBRACKET expression-list CLOSESQUAREBRACKET array-initializer-opt
			 '''

def p_expression_list(p):
	''' expression-list :         expression
			 |         expression-list COMMA expression
			 '''
	if len(2):
		p[0] = [p[1]]
	elif len(4):
		p[0] = p[1] + [p[3]]
	
def p_array_initializer_opt(p):
	''' array-initializer-opt :         array-initializer
			 |         empty
			 '''
	

def p_array_initializer(p):
	''' array-initializer :         BLOCKBEGIN variable-initializer-list-opt BLOCKEND
			 '''
	

def p_variable_initializer_list_opt(p):
	''' variable-initializer-list-opt :         variable-initializer-list
			 |         empty
			 '''
	
	
def p_variable_initializer_list(p):
	''' variable-initializer-list :         variable-initializer
			 |         variable-initializer-list COMMA variable-initializer
			 '''
	
	
def p_variable_initializer(p):
	''' variable-initializer :         expression
			 |         array-initializer
			 '''
	p[0] = p[1]

def p_primary_no_array_creation_expression_literal(p):
	''' primary-no-array-creation-expression :         literal
			 '''
	p[0]={}
	p[0] = p[1]

def p_primary_no_array_creation_expression_identifier(p):
	''' primary-no-array-creation-expression :         IDENTIFIER
			 '''
	p[0]={}
	if ST.exists(p[1]):
		p[0]['place'] = p[1]
		p[0]['type']  = ST.getAttribute(p[1],'type')
		p[0]['initializer'] = ST.getAttribute(p[1],'initializer')
		
	else:
		debug("identifier " + p[1] +" is not initialize "+ str(p.lexer.lineno))

def p_primary_no_array_creation_expression_pExpression(p):
	''' primary-no-array-creation-expression :        parenthesized-expression
			 '''	
	p[0] = p[1]

def p_primary_no_array_creation_expression_invocation(p):
	''' primary-no-array-creation-expression :      invocation-expression
			 '''
	p[0] = p[1]

def p_parenthesized_expression(p):
	''' parenthesized-expression :         OPENPARENTHESIS expression CLOSEPARENTHESIS
			 '''
	p[0] = p[1]

def p_invocation_expression(p):
	''' invocation-expression :         IDENTIFIER OPENPARENTHESIS argument-list-opt CLOSEPARENTHESIS
			 '''
	if ST.exists(p[1]):
		for param in p[3]:
			TAC.emit(param['place'],'','','param')
		TAC.emit(p[1],'','','callFunc')
	else:
		debug("Function " +p[1]+" not exist")

def p_argument_list_opt(p):
	''' argument-list-opt :         argument-list
			 |         empty
			 '''
	p[0] = p[1]
	
def p_argument_list(p):
	''' argument-list :         argument
			 |         argument-list COMMA argument
			 '''
	if len(p) == 2:
		p[0]=[p[1]]
	elif len(p) == 4:
		p[0] = p[1]+[p[3]]

	
def p_argument(p):
	''' argument :         expression
			 '''
	p[0] = p[1]
		
def p_post_increment_expression(p):
	''' post-increment-expression :         primary-expression INCREMENT
			 '''
	p[0]=p[1]
	if ST.exists(p[1]['place']):
		if ST.getAttribute(p[1]['place'],'type') == 'int':
			TAC.emit(p[1]['place'],p[1]['place'],'1','+')
		else:
			debug('type error at line no ' + str(p.lexer.lineno))
	else:
		debug(p[1]['place'] + 'identifier not exist')

def p_post_decrement_expression(p):
	''' post-decrement-expression :         primary-expression DECREMENT
			 '''
	p[0]=p[1]
	if ST.exists(p[1]['place']):
		if ST.getAttribute(p[1]['place'],'type') == 'int':
			TAC.emit(p[1]['place'],p[1]['place'],'1','-')
		else:
			debug('type error at line no ' + str(p.lexer.lineno))
	else:
		debug(p[1]['place'] + 'identifier not exist')

def p_pre_increment_expression(p):
	''' pre-increment-expression :         INCREMENT unary-expression
			 '''
	p[0]=p[2]
	if ST.exists(p[2]['place']):
		if ST.getAttribute(p[2]['place'],'type') == 'int':
			TAC.emit(p[2]['place'],p[2]['place'],'1','+')
		else:
			debug('type error at line no ' + str(p.lexer.lineno))
	else:
		debug(p[2]['place'] + 'identifier not exist')

def p_pre_decrement_expression(p):
	''' pre-decrement-expression :         DECREMENT unary-expression
			 '''
	p[0]=p[2]
	if ST.exists(p[2]['place']):
		if ST.getAttribute(p[2]['place'],'type') == 'int':
			TAC.emit(p[2]['place'],p[2]['place'],'1','-')
		else:
			debug('type error at line no ' + str(p.lexer.lineno))
	else:
		debug(p[2]['place'] + 'identifier not exist')

def p_assignment(p):
	''' assignment :         primary-expression assignment-operator expression
			 '''
	p[0] = {}
	# print p[3]
	p[0]['place'] = ST.newTemp()
	if p[1]['type'] == p[3]['type']:
		if p[3]['initializer'] == 1:
			ST.addAttribute(p[1]['place'],'initializer',1)
			TAC.emit(p[1]['place'], p[3]['place'],' ', p[2])
		else:
		 debug (p[3]['place']+ "  not initializer in expression at "  + str(p.lexer.lineno))
		 p[0]['type'] = p[1]['type']
	else:
		debug("type error in assignment-operator " + str(p.lexer.lineno))
		p[0]['type']= 'none'
		ST.addIdentifier(p[0]['place'],p[0]['type'])

def p_assignment_operator(p):
	''' assignment-operator :         ASSIGN
			 |         PLUSEQUAL
			 |         MINUSEQUAL
			 |         MULTIPLYEQUAL
			 |         DIVIDEEQUAL
			 |         MODULUSEQUAL
			 |         ANDEQUAL
			 |         OREQUAL
			 |         XOREQUAL
			 |         LEFTSHIFTEQUAL
			 |         RIGHTSHIFTEQUAL
			 '''
	p[0] = p[1]
	
def p_field_declaration(p):
	''' field-declaration :      type variable-declarators SEMICOLON
			 '''
	
def p_variable_declarators(p):
	''' variable-declarators :         variable-declarator
			 |         variable-declarators COMMA variable-declarator
			 '''	

def p_variable_declarator(p):
	''' variable-declarator :         IDENTIFIER
			 |         IDENTIFIER ASSIGN variable-initializer
			 '''

def p_method_declaration(p):
	''' method-declaration :         method-header method-body
			 '''
	
	if p[1] == "Main":
		TAC.emit('','','','exit')
	elif p[1] != "Main":
		TAC.emit('','','','ret')
	# ST.addScope('it','void')
	ST.deleteScope(p[2])


def p_method_header(p):
	''' method-header :  type member-name OPENPARENTHESIS formal-parameter-list-opt CLOSEPARENTHESIS
			 |         VOID member-name OPENPARENTHESIS formal-parameter-list-opt CLOSEPARENTHESIS
			 '''
	p[0] = {}
	p[0] = p[2]
	if p[2] == "Main":
		TAC.emit('','','','Main_Level:')
	elif p[2] != "Main":
		TAC.emit('',p[2]+':','','funcLabel')
		# print p[2]
		# print p[1]['type']
		ST.addScope(p[2],p[1]['type'])

		for parameter in p[4]:
			ST.addIdentifier(parameter['identifier_name'],parameter['type'])


def p_formal_parameter_list_opt(p):
	''' formal-parameter-list-opt :         formal-parameter-list
			 |         empty
			 '''
	p[0] = p[1]
	
def p_member_name(p):
	''' member-name :         IDENTIFIER
			 '''
	p[0] = p[1]

def p_formal_parameter_list(p):
	''' formal-parameter-list :         fixed-parameters
			 '''
	p[0] = p[1]

def p_fixed_parameters(p):
	''' fixed-parameters :         fixed-parameter
			 |         fixed-parameters COMMA fixed-parameter
			 '''
	if len(p) == 2:
		p[0] = [p[1]]
	elif len(p) == 4:
		p[0] == p[1] + [p[3]]

def p_fixed_parameter(p):
	''' fixed-parameter :         type IDENTIFIER
			 '''
	p[0] = { 'identifier_name' : p[2], 'type':p[1]['type']}

	
def p_method_body(p):
	''' method-body : block
					| SEMICOLON
			 '''
	p[0] = p[1]

def p_block(p):
	''' block :         BLOCKBEGIN statement-list-opt BLOCKEND
			 '''
	p[0] = p[1]

def p_statement_list_opt(p):
	''' statement-list-opt :         statement-list
			 |         empty
			 '''
	p[0] = p[1]

def p_statement_list(p):
	''' statement-list :         statement
			 |         statement-list statement
			 '''
	p[0] = {}
	if len(p) == 2:
		p[0] = [p[1]]
	elif len(p) == 3:
		p[0] = p[1] + [p[2]]


def p_statement(p):
	''' statement :     declaration-statement
			 |         embedded-statement
			 |		   read-statement
			 |         write-statement
			 '''
	p[0] = p[1]

	
def p_declaration_statement(p):
	''' declaration-statement :         local-variable-declaration SEMICOLON
			 |         local-constant-declaration SEMICOLON 
			 '''
	p[0] = p[1]
	
def p_local_variable_declaration(p):
	''' local-variable-declaration :         type local-variable-declarators
			 '''
	for identifier in p[2]:
		if not ST.existsInCurrentScope(identifier['identifier_name']):
			ST.addIdentifier(identifier['identifier_name'], p[1]['type'])
			ST.addAttribute(identifier['identifier_name'], 'initializer', identifier['initializer'])
		else:
		 debug(" identifier already declar " + identifier["identifier_name"])

	
def p_local_variable_declarators(p):
	''' local-variable-declarators :         local-variable-declarator
			 |         local-variable-declarators COMMA local-variable-declarator
			 '''
	if len(p) == 2:
		p[0] = [p[1]]
	elif len(p) == 4:
		p[0] = p[1] + [p[3]] 


def p_local_variable_declarator(p):
	''' local-variable-declarator :         IDENTIFIER
			 |         IDENTIFIER ASSIGN local-variable-initializer
			 '''

	if len(p) == 2:
		p[0] = {'identifier_name' : p[1], 'initializer' : 0}
	elif len(p) == 4:
		p[0] = { 'identifier_name' : p[1], 'initializer' : 1}
		TAC.emit(p[1],p[3]['place'],'',p[2])
	
def p_local_variable_initializer(p):
	''' local-variable-initializer :         expression
			 |         array-initializer
			 '''
	p[0] = p[1]

def p_local_constant_declaration(p):
	''' local-constant-declaration :         CONST type constant-declarators
			 '''
	
def p_embedded_statement(p):
	''' embedded-statement :         block
			 |         empty-statement
			 |         expression-statement
			 |         selection-statement
			 |         iteration-statement
			 |         jump-statement
			 '''
def p_write_statement(p):
    ''' write-statement :         CONSOLE DOT WRITELINE OPENPARENTHESIS print-list CLOSEPARENTHESIS SEMICOLON
             '''
    p[0] = {}
    p[0]['type'] = 'void'
    for var in p[5]:
    	if var['type'] == 'int':
    		TAC.emit(var['place'],'','','PrintInt')
    	elif var['type'] == 'float':
    		TAC.emit(var['place'],'','','PrintFloat')
    	elif var['type'] == 'char':
    		TAC.emit(var['place'],'','','PrintChar')
    	elif var['type'] == 'string':
    		# print var
    		TAC.emit(var['place'],'','','PrintString')


def p_print_list(p):
    ''' print-list :         expression
             |         expression COMMA print-list 
             '''
    if len(p) == 2:
    	p[0] = [p[1]]
    elif len(p) == 4:
    	p[0] = [p[1]] + p[3]

def p_read_statement(p):
    ''' read-statement :         CONSOLE DOT READLINE OPENPARENTHESIS IDENTIFIER CLOSEPARENTHESIS SEMICOLON
             '''
    if ST.exists(p[5]):
    	TAC.emit('','',p[5],'Read')
    p[0]['type'] = 'void'
	
def p_empty_statement(p):
	''' empty-statement :         SEMICOLON
			 '''
	p[0] = {}
	p[0]['type'] = 'void'

def p_expression_statement(p):
	''' expression-statement :         statement-expression SEMICOLON
			 '''
	p[0] = p[1]

def p_statement_expression(p):
	''' statement-expression :         invocation-expression
			 |         assignment
			 |         post-increment-expression
			 |         post-decrement-expression
			 |         pre-increment-expression
			 |         pre-decrement-expression
			 '''
	p[0] = p[1]

def p_selection_statement(p):
	''' selection-statement :         if-statement
							| 		switch-statement
			 '''
	p[0] = {}
	p[0] = p[1]
	# print p[1]
	# if p[1]['type'] == 'void':
	# 	p[0]['type'] = 'void'
	# else:
		# debug('type error at ' + str(p.lexer.lineno))

def p_if_statement(p):
	''' if-statement :         IF OPENPARENTHESIS boolean-expression CLOSEPARENTHESIS embedded-statement
			 '''
	TAC.emit(level['sElse'],'','','level')

def p_elif_statement(p):
	''' if-statement :         IF OPENPARENTHESIS boolean-expression CLOSEPARENTHESIS  embedded-statement ELSE l_else block
			 '''
	TAC.emit(level['sAfter'],'','','level')		

def p_L_else(p):
	''' l_else : empty'''
	TAC.emit(level['sAfter'],'','','goto')
	TAC.emit(level['sElse'],'','','level')		
	
def p_boolean_expression(p):
	''' boolean-expression :         expression
			 '''
	level['sElse'] = ST.newLevel()
	level['sAfter'] = ST.newLevel()
	TAC.emit(level['sElse'],p[1]['place'],0,'ifgoto')

def p_switch_statement(p):
    ''' switch-statement :         SWITCH OPENPARENTHESIS expression  CLOSEPARENTHESIS  switch-lavel-end switch-block
             '''
    p[0] = {}
    # print p[3]
    # print p[6]
    # if p[3]['type'] == p[6]['type']:
    # 	p[0]['type'] = 'void'
    TAC.emit('switch_level','','','level')
    for var in p[6]['cases']:
    	# print var
    	if var['place']:
    		temp = ST.newTemp()
    		TAC.emit(temp,var['place'],p[3]['place'],'==')
    		ST.addIdentifier(temp,p[3]['type'])
    		TAC.emit(var['addr'],temp,'1','ifgoto')
    	else:
            TAC.emit(var['addr'],'','','goto')
    
    TAC.emit(level['switch-after'],'','','level')

# def p_Switch_start(p):
# 	'switch-start : empty'
# 	TAC.emit('switch-label','','','goto')
def p_M_end(p):
	'switch-lavel-end : empty'
	
	level['switch-after'] = ST.newLevel()
	TAC.emit('switch_level','','','goto')


def p_switch_block(p):
    ''' switch-block :         BLOCKBEGIN  switch-sections BLOCKEND 
             '''
    p[0] = p[2]
    # print p[2]
def p_switch_sections(p):
    ''' switch-sections :         switch-section
             |         switch-sections switch-section
             '''
    if len(p) == 2:
    	p[0] = p[1]
    elif len(p) == 3:
    	p[0] = {}
    	p[0]['cases'] = p[1]['cases'] + p[2]['cases']
    # print p[0]
def p_switch_section(p):
    ''' switch-section :         switch-label M-switch statement-list
             '''
    
    p[0]={}
    # p[0] = p[1]
    p[0]['cases']=[{'place':p[1]['place'],'addr':p[2],'type':p[1]['type']}]
    TAC.emit(level['switch-after'],'','','goto')
    # print p[0]

def p_M_switch(p):
	'M-switch : empty '
	p[0] = ST.newLevel()
	TAC.emit(p[0],'','','level')

def p_switch_label(p):
    ''' switch-label :         CASE expression COLON
             |         DEFAULT COLON
             '''
    if len(p)==4:
        p[0]=p[2] #gives value and type
    else:
        p[0]={'place':None,'type':None}	

def p_iteration_statement(p):
	''' iteration-statement :         while-statement
			 |         do-statement
			 |			for-statement
			 '''
	p[0] = {}
	p[0] = p[1]
	if p[1]['type'] == 'void':
		p[0]['type'] = 'void'
	else:
		debug('type error at ' + str(p.lexer.lineno))

def p_while_statement(p):
	''' while-statement : WHILE M_while OPENPARENTHESIS M-while-expression CLOSEPARENTHESIS embedded-statement
			 '''
	p[0] = {}
	p[0]['type'] = 'void' 
	TAC.emit(level['wBegin'],'','','goto')
	TAC.emit(level['wElse'],'','','level')

def p_while_expression(p):
	'''M-while-expression : expression '''

	level['wElse'] = ST.newLevel()
	level['sAfter'] = ST.newLevel()
	TAC.emit(level['wElse'],p[1]['place'],0,'ifgoto')
	# TAC.emit(level['wBegin'],'','','goto')



def p_M_while(p):
	'''	M_while : empty '''	
	level['wBegin'] = ST.newLevel()
	TAC.emit(level['wBegin'],'','','level')

def p_do_statement(p):
	''' do-statement : DO embedded-statement WHILE OPENPARENTHESIS boolean-expression CLOSEPARENTHESIS SEMICOLON
			 '''
	
def p_do_statement_error(p):
	''' do-statement : DO embedded-statement WHILE OPENPARENTHESIS boolean-expression CLOSEPARENTHESIS error
			 '''
	print 'Semicolon is missing in do-while loop in lineno ' + str(p.lineno(1))

def p_for_statement_error1(p):
    ''' for-statement : FOR OPENPARENTHESIS for-initializer-opt error for-condition-opt SEMICOLON for-iterator-opt CLOSEPARENTHESIS embedded-statement
             '''
    print 'first Semicolon missing in for-loop lineno'+ str(p.lineno(1))
def p_for_statement_error2(p):
    ''' for-statement : FOR OPENPARENTHESIS for-initializer-opt SEMICOLON for-condition-opt error for-iterator-opt CLOSEPARENTHESIS embedded-statement
             '''
    print 'Second Semicolon missing in for-loop lineno'+ str(p.lineno(1))


def p_for_statement(p):
    ''' for-statement : FOR OPENPARENTHESIS for-initializer-opt SEMICOLON for-condition-opt SEMICOLON for-iterator-opt CLOSEPARENTHESIS embedded-statement
             '''
    TAC.emit(level['for_condition_level'],'','','goto')
    TAC.emit(level['for_end'],'','','level')
    p[0] = {}
    p[0]['type'] = 'void' 

def p_for_initializer_opt(p):
    ''' for-initializer-opt :         for-initializer
             |         empty
             '''
    p[0] = p[1]
    level['for_end'] = ST.newLevel()
    level['for_start'] = ST.newLevel()
    level['for_block_start'] = ST.newLevel()
    TAC.emit(level['for_start'],'','','level')

def p_for_initializer(p):
    ''' for-initializer :         local-variable-declaration
             |  	     expression
             '''
    p[0] = p[1]

def p_for_condition_opt(p):
    ''' for-condition-opt :         for-condition
             |         empty
             '''
    p[0] =p[1]
    TAC.emit(level['for_block_start'],p[1]['place'],'1','ifgoto')
    TAC.emit(level['for_end'],'','','goto')
    level['for_condition_level'] = ST.newLevel()
    TAC.emit(level['for_condition_level'],'','','level')

def p_for_condition(p):
    ''' for-condition :         for-boolean-expression
             '''
    p[0] = p[1]

def p_for_boolean_expression(p):
	'for-boolean-expression : expression '

	p[0] = p[1]

def p_for_iterator_opt(p):
    ''' for-iterator-opt :         for-iterator
             |         empty
             '''

    p[0] = p[1]
    TAC.emit(level['for_start'],'','','goto')
    TAC.emit(level['for_block_start'],'','','level')

def p_for_iterator(p):
    ''' for-iterator :         expression
 		            '''
    p[0] = p[1]	

def p_jump_statement(p):
	''' jump-statement :         break-statement
			 |         continue-statement
			 |         goto-statement
			 |         return-statement
			 '''
	p[0] = {}
	p[0]['type'] = 'void'

def p_break_statement(p):
	''' break-statement :         BREAK SEMICOLON
			 '''
	
def p_continue_statement(p):
	''' continue-statement :         CONTINUE SEMICOLON
			 '''
	
def p_goto_statement(p):
	''' goto-statement :         GOTO IDENTIFIER SEMICOLON
			 '''
	
def p_goto_statement_error(p):
	''' goto-statement :         GOTO IDENTIFIER error
			 '''
	print 'semicolon missing in goto stat'
def p_return_statement(p):
	''' return-statement :         RETURN expression SEMICOLON
			 '''

	TAC.emit(p[2]['place'],'','','ret')

	
def p_literal_int(p):
	''' literal :     SIGNEDINTEGER
			 |     UNSIGNEDINTEGER
			 |     LONGINTEGER
			 |     UNSIGNEDLONGINTEGER	         '''
	p[0] = {}
	p[0]['type'] = 'int'
	var = ST.newTemp()
	TAC.emit(var,p[1],' ','=')
	ST.addIdentifier(var,p[0]['type'])
	p[0]['place'] = var
	p[0]['initializer'] = 1	

def p_literal_float(p):
	''' literal :    FLOATREAL
			 |     DOUBLEREAL
			 |     DECIMALREAL
	          '''
	p[0] = {}
	p[0]['type'] = 'float'
	var = ST.newTemp()
	TAC.emit(var,p[1],' ','=')
	p[0]['place'] = var
	p[0]['initializer'] = 1
	ST.addIdentifier(var,p[0]['type'])

def p_literal_char(p):
	''' literal :     CHARACTER     '''
	p[0] = {}
	p[0]['type'] = 'char'
	var = ST.newTemp()
	TAC.emit(var,p[1],' ','=')
	p[0]['place'] = var
	# print var + "lalu" +p[1]
	p[0]['initializer'] = 1
	ST.addIdentifier(var,p[0]['type'])

def p_literal_string(p):
	''' literal :    REGULARSTRING
			 |     VERBATIMSTRING             '''
	p[0] = {}
	p[0]['type'] = 'string'
	p[0]['str'] = ST.newString(p[1])
	# print p[1]
	p[0]['place'] = ST.newString(p[1])
	p[0]['initializer'] = 1
	ST.addIdentifier(p[0]['place'],p[0]['type'])

def p_literal_bool(p):
	''' literal :     TRUE
			 |     FALSE             '''
	p[0] = {}
	var = ST.newTemp()
	TAC.emit(var,p[1],' ','=')
	p[0]['place'] = var
	p[0]['type'] = 'bool'
	p[0]['initializer'] = 1
	ST.addIdentifier(var,p[0]['type'])
	
	
def p_empty(p):
	'empty :'
	p[0] = {}
	pass
def p_type(p):
	''' type :         simple-type
			 |         array-type
			 '''
	p[0] = p[1]
	
	
def p_numeric_type(p):
	''' simple-type :         integral-type
			 |         floating-point-type
			 '''
	p[0] = p[1]
	
def p_integral_type(p):
	''' integral-type :         INT
			 |         CHAR
			 | 			BOOL
			 |			STRING
			 '''
	p[0] = {}
	p[0]['type'] = p[1]

def p_floating_point_type(p):
	''' floating-point-type :         FLOAT
			 |         DOUBLE
			 '''
	p[0] = {}
	p[0]['type'] = 'float'

def p_array_type(p):
	''' array-type :         simple-type rank-specifier
			 '''
	
def p_rank_specifier(p):
	''' rank-specifier :         OPENSQUAREBRACKET dim-separators-opt CLOSESQUAREBRACKET
			 '''
	
def p_dim_separators_opt(p):
	''' dim-separators-opt :         dim-separators
			 |         empty
			 '''
	
def p_dim_separators(p):
	''' dim-separators :         COMMA
			 |         dim-separators COMMA
			 '''
	
def p_error(p):
	if p:
		print "Syntax error at line " + str(p.lineno)
		print 'Token : {}'.format(p)
	else:
		print("Syntax error!")
	
	while 1:
		tok = yacc.token()
		if tok:
			if tok.type in ['SEMICOLON','BLOCKEND']:
				a=0
				break
		yacc.errok()
		# tok = yacc.token()
		# yacc.restart()
	return tok


parser = yacc.yacc()

def parseProgram(input):
	parser.parse(input, lexer=lexer)
	return TAC, ST
    

if __name__ == '__main__':
	input_ = open(argv[1]).read()
	parseProgram(input_)
	# output = parser.parse(input_,lexer=lexer, debug=False, tracking=True)
	# TAC.printCode()
	print ST.string
	for i in range(len(TAC.code)):
            print i, TAC.code[i]
