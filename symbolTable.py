import pprint

class SymbolTable:
    # Constructor for the function
    def __init__(self):
        self.symbolTable = {
                'main': {
                    '__scopeName__': 'main', 
                    '__parentName__': 'main', 
                    '__type__':'FUNCTION', 
                    '__returnType__': 'UNDEFINED',
                    '__level__' : 0
                    }
                }
        self.temporaryCount = 0
        self.functionList = { 'main': self.symbolTable['main']}
        self.charSize = 1
        self.booleanSize = 4
        self.undefinedSize = 0
        self.intSize = 4
        self.levelBase = "level"
        self.levelCount = 0
        self.string = {}

        # Two stacks one for offset and other for the current scope
        self.offset = [0]
        self.scope = [self.symbolTable['main']]

        # For creating the temporaries
        self.tempBase = "t"
        self.tempCount = 0

        # For creating the string
        self.stringBase = "string"
        self.stringCount = 0

    # Print the symbolTable
    def printSymbolTable(self):
        pprint.pprint(self.symbolTable)
        # print self.symbolTable['main']['i']['__offset__']

    def returnOffset(self,var):
        return 1


    def printFunctionList(self):
        pprint.pprint(self.functionList)
    # function to return currentScope name
    def getCurrentScope(self):
        return self.scope[len(self.scope) - 1]['__scopeName__']

    # function to lookup an element in the stack
    def lookup(self, identifier):
        # Obtain the currentScope
        scopeLocation = len(self.scope)
        # print scopeLocation  
        return self.lookupScope(identifier, scopeLocation - 1)

    def lookupScope(self, identifier, scopeLocation):
        if scopeLocation == -1:
            return None

        # add the scope to the symbolTable
        currentScope = self.scope[scopeLocation]
        if currentScope.has_key(identifier):
            return currentScope[identifier]
        else:
            return self.lookupScope(identifier, scopeLocation - 1)

    # function to add a Scope
    def addScope(self, functionName, functionType):
        # add the scope to the symbolTable
        currentScope = self.scope[len(self.scope) - 1]
        level = currentScope['__level__'] + 1

        currentScope[functionName] = {
                '__scopeName__': functionName, 
                '__parentName__': currentScope['__scopeName__'],
                '__returnType__': functionType,
                '__type__': 'FUNCTION',
                '__level__' : level
                }
        self.scope.append(currentScope[functionName])

        # Marks a new relative address
        self.offset.append(0)
        self.functionList[functionName] = currentScope[functionName]

    # function to delete a scope
    def deleteScope(self, functionName):
        # Update the width of the function
        currentScope = self.scope.pop()
        currentScope['__width__'] = self.offset.pop()

    # function to add an element to the current scope
    def addIdentifier(self, identifier, IdentifierType, IdentifierWidth=0):
        # add the scope to the symbolTable
        currentScope = self.scope[len(self.scope) - 1]

        # Ladder to decide the width of the Identifier
        if IdentifierWidth == 0:
            if IdentifierType == 'char':
                IdentifierWidth = self.charSize
            elif IdentifierType == 'bool':
                IdentifierWidth = self.booleanSize
            elif IdentifierType == 'int':
                IdentifierWidth = self.intSize
            else:
                # For UNDEFINED
                IdentifierWidth = self.undefinedSize

        # increment the offset of the top
        currentOffset = self.offset.pop()

        # Update the entry
        if not currentScope.has_key(identifier):
            currentScope[identifier] = {}

        currentScope[identifier]['__width__'] = IdentifierWidth
        currentScope[identifier]['__type__'] = IdentifierType
        currentScope[identifier]['__offset__'] = currentOffset
        currentScope[identifier]['__scopeLevel__'] = currentScope['__level__']

        self.offset.append(currentOffset + IdentifierWidth)

    # add an attribute to the identifier
    def addAttribute(self, identifier, attributeName, attributeValue):
        entry = self.lookup(identifier)
        entry['__' + attributeName + '__'] = attributeValue

    def addAttributeToCurrentScope(self, attributeName, attributeValue):
        currentScope = self.scope[len(self.scope) - 1]
        currentScope['__' + attributeName + '__'] = attributeValue

    def getAttributeFromCurrentScope(self, attributeName):
        currentScope = self.scope[len(self.scope) - 1]
        return currentScope[ '__' + attributeName + '__']

    def getFunctionAttribute(self, identifier, attribute):
        functionName = self.getAttribute(identifier, 'name')
        if self.functionList.has_key(functionName):
            return self.functionList[functionName]['__' + attribute + '__']
        else:
            return None

    # Get the attribute of a given identifier
    def getAttribute(self, identifier, attributeName):
        # identifier = 'i'
        identifierEntry = self.lookup(identifier)
        # print identifierEntry
        if identifierEntry.has_key('__' + attributeName + '__'):
            return identifierEntry['__' + attributeName + '__']
        else:
            return None

    # Function to check if an identifier exists in the lexical scope or not
    def exists(self, identifier):
        identifierEntry = self.lookup(identifier)
        if identifierEntry != None:
            return True
        else:
            return False

    # Lookup the variable in the current scope
    def existsInCurrentScope(self, identifier):
        return self.scope[len(self.scope) - 1].get(identifier, False) != False
        
    def getAttributeFromFunctionList(self, function, attributeName):
        if self.functionList.has_key(function):
            return self.functionList[function]['__' + attributeName + '__']
        else:
            return None

    # Function to create new temporaries
    def newTemp(self, memoryLocation='', variable='', loadFromMemory=False):
        self.tempCount = self.tempCount + 1
        createdTemp = self.tempBase + str(self.tempCount)
        return createdTemp

    def newLevel(self):
        self.levelCount += 1
        createdLevel =  self.levelBase + str(self.levelCount) 
        return createdLevel 

    def newString(self,stringValue):
        self.stringCount +=1
        createString = self.stringBase + str(self.stringCount)
        self.string[createString] = stringValue
        return createString 