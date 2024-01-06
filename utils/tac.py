class ThreeAddressCode:
    def __init__(self):
        self.code = []

    def emit(self, regDest, regSrc1, regSrc2, op):
        self.code.append([op, regSrc1, regSrc2, regDest])

    def printCode(self, fileName=""):
        for i in range(len(self.code)):
            print(i, self.code[i])
