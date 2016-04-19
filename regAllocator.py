import symbolTable as SymbolTable
import pprint
# import codegen1

# ST = SymbolTable.SymbolTable()

class regAllocator:

	def __init__(self):
		self.ST = {}
		self.varDescripter = {}
		self.regDescripter = {}
		self.usedReg = []
		self.asmInstr = ""
		self.code = []
		self.func = []
		self.freeReg = ["$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7","$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7"]

	def prints(self,st,function):
		self.ST = st
		self.func = function
		# print st
		# print self.func[-1]
	def getRegister(self,arg,offset):
		var=arg

		fname =  'main'
		# print fname
		# fName = 
		# self.ST.printSymbolTable()
		# print ST.symbolTable['main']['t3']['offset'] 

		# print self.ST
		for key,value in self.regDescripter.iteritems():
			if value == var:
				return key

		if len(self.freeReg) > 0:	#if there is a register available
			# print "freereg"+arg
			reg = self.freeReg.pop(0)	#pop a free register
			self.usedReg.append(reg)	#append that register to list of used registers
			self.regDescripter[reg] = arg	#this register now contains value of arg
			self.varDescripter[var] = reg   #this variable is now contained in reg 
			return reg

		elif len(self.freeReg) == 0:	#if no register is available
			# print "not free"
			
			reg = self.usedReg.pop(0)
			self.regDescripter[reg] = arg
			for key,value in self.varDescripter.iteritems():	#find the variable for which this register was being used. nullify it
				if value == reg:
					self.varDescripter[key] = ""
					# print "var" + key +" "+ "arg" + arg
					if fname == 'main':
						offset_key = self.ST[fname][key]['__offset__']
						offset_arg = self.ST[fname][arg]['__offset__']
					else:
						offset_key = self.ST['main'][fname][key]['__offset__']
						offset_arg = self.ST['main'][fname][arg]['__offset__'] 
					# print ST.symbolTable['main']['t1']['offset'] +"blallalalalal"
					# key_offset=ST.returnOffset(key)
					# print key_offset +"gi"
					self.code.append("sw "+reg+", "+str(offset_key)+"($sp)")
					self.code.append("lw "+reg+", "+str(offset_arg)+"($sp)")

			self.varDescripter[var] = reg      #set this variable to be contained in register
			# print "dsb "+reg 
			
			return reg