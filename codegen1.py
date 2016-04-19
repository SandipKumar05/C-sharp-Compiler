import sys
import regAllocator
import ply.yacc as yacc
import lexer
from sys import argv
import symbolTable as SymbolTable
from tac import *
import parser 


# ST = SymbolTable.SymbolTable()
TAC = ThreeAddressCode()

mips = regAllocator.regAllocator()
func = ['main']


def convertToAsm(line,lineNum):
	global exitFound
	asmInstruc = ""
	word = line
	# print ST.returnOffset("t3")

	if word[0] == "#":
		#comment
		pass
	elif word[0] == "Main_Level:":
		mips.code.append("main:")
		# print func
		mips.prints(ST.symbolTable,func)

		# func.append("foo")
		# print func[0]
		# ST.printSymbolTable()
		# key_offset=ST.getAttribute('t1', "offset")
		# print ST.getAttribute('t1','type')


	elif word[0] == "=":
		
		
		if word[1].isdigit():
			reg1 = mips.getRegister(word[3],ST.returnOffset(word[3]))
			mips.code.append("li "+reg1+","+str(word[1]))
		else:
			reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
			reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
			mips.code.append("move "+reg2+","+reg1)
	elif word[0] == "PrintInt":
		mips.code.append("li $v0,1")
		reg1 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append("move $a0,"+reg1)
		mips.code.append("syscall")

	elif word[0] == "PrintString":
		mips.code.append("li $v0,4")
		sname = ""
		for key, value in ST.string.iteritems():
			if value == '"'+word[3]+'"':
				sname = key
		# reg1 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append("la $a0, "+key)
		mips.code.append("syscall")
		sname = ""

	elif word[0] == "exit":
		mips.code.append("li $v0, 10")
		mips.code.append("syscall")
	elif word[0] == '+':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append("add "+ reg3 + ", " + reg1 +", "+reg2)
	elif word[0] == '-':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append("sub "+ reg3 + ", " + reg1 +", "+reg2)

	elif word[0] == 'goto':
		mips.code.append("b"+" "+ word[3])

	elif word[0] == 'level':
		mips.code.append(word[3]+':')

	elif word[0] == 'ifgoto':
		# print word[2]
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		if word[2] == 0:
			# print "hello"
			mips.code.append('beqz '+reg1+ ' '+	word[3])
		elif word[2] == '1':
			# print "hello"+"jbjhb"
			mips.code.append('bnez '+reg1+ ' '+	word[3])
	elif word[0] == '*':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('mult '+reg1+', '+reg2)
		mips.code.append('mflo '+reg3)
	elif word[0] == '/':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('div '+reg1+', '+reg2)
		mips.code.append('mflo '+reg3)

	elif word[0] == '%':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('div '+reg1+', '+reg2)
		mips.code.append('mfhi '+reg3)

	elif word[0] == '+=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('add '+reg2+', '+reg2+', '+reg1)

	elif word[0] == '|':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('or '+reg3+', '+reg1+', '+reg2)
	
	elif word[0] == '^':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('xor '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '&':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('and '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '==':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('seq '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '!=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('sne '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '<':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('slt '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '>':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('sgt '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '<=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('sle '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '>=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('sge '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '<<':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('sllv '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '>>':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[2],ST.returnOffset(word[2]))
		reg3 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('srlv '+reg3+', '+reg1+', '+reg2)

	elif word[0] == '-=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('sub '+reg2+', '+reg2+', '+reg1)

	elif word[0] == '*=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('mult '+reg2+', '+reg1)
		mips.code.append('mflo '+reg2)

	elif word[0] == '/=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('div '+reg2+', '+reg1)
		mips.code.append('mflo '+reg2)

	elif word[0] == '%=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('div '+reg2+', '+reg1)
		mips.code.append('mfhi '+reg2)

	elif word[0] == '^=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('xor '+reg2+', '+reg2+', '+reg1)

	elif word[0] == '|=':
		reg1 = mips.getRegister(word[1])
		reg2 = mips.getRegister(word[3])
		mips.code.append('or '+reg2+', '+reg2+', '+reg1)

	elif word[0] == '&=':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('and '+reg2+', '+reg2+', '+reg1)

	elif word[0] == '<<==':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('sllv '+reg2+', '+reg2+', '+reg1)

	elif word[0] == '>>==':
		reg1 = mips.getRegister(word[1],ST.returnOffset(word[1]))
		reg2 = mips.getRegister(word[3],ST.returnOffset(word[3]))
		mips.code.append('srlv '+reg2+', '+reg2+', '+reg1)

	elif word[0] == 'funcLabel':
		mips.code.append(word[1])
		func.append(word[1])
		
	elif word[0] == 'callFunc':
		regDesc = mips.regDescripter
		for key,value in regDesc.iteritems():
			mips.code.append("addi $sp,$sp,-4")
			mips.code.append("sw "+key+",($sp)")
		mips.code.append("addi $sp,$sp,-4")
		mips.code.append("sw $ra,($sp)")
		mips.code.append("jal "+word[3])
		mips.code.append("lw $ra,($sp)")
		mips.code.append("addi $sp,$sp,4")

		for key,value in regDesc.iteritems():

			mips.code.append("lw "+key+",($sp)")
			mips.code.append("addi $sp,$sp,4")

	elif word[0] == "ret":
		# print word[3]
		# mips.code.append("lw $v0,"+word[3])
		mips.code.append("jr $ra")

		func.pop()




outputMain = []
outputData = []
outputText = []
exitFound = False
regDesc = []
varList = []
initList = []
tacString = ""

if __name__ == '__main__':
	input_ = open(argv[1]).read()

	TAC, ST = parser.parseProgram(input_)
	
	outputData.append(".data")
	mips.code.append(".text")
	# printsym()
	# ST.printSymbolTable()
	# ST.printFunctionList()
	# mips.code.append("main:")
	# print str(ST.getAttributeFromFunctionList('main','width'))
	mips.code.append('sub $sp, $sp, '+str(ST.getAttributeFromFunctionList('main','width')))
	mips.code.append('b '+ 'main')
	# mips.code.append('add $sp, $sp, '+str(ST.getAttributeFromFunctionList('main','width')))
	mips
	lineNum = 0
	# print ST.string
	# print ST.string
	for i in ST.string:
		# print ST.string[i]
		outputData.append(i+':'+" .asciiz " + ST.string[i]) 

	for line in TAC.code:
		lineNum = lineNum +1
		# print line
		convertToAsm(line,lineNum)
	f=open('hello.spim', 'wb')
	for i in outputData + mips.code:
			f.write(i+'\n')
	f.close()
