#!/usr/bin/env python
from SourceCodeCtx import SourceCodeCtx
from Model import Model
from Generator import Generator

def testPython():
    tet = input("test input\n")
    print(tet,end="")
    print("testend")
    testlist = [1,2,3,4,5,6]
    print(testlist[0:-1])

    testlist = [ testlist[num - 1] for num in range(1,len(testlist) + 1)
            if num < 3 or num > 5]

def testContext():
    sourceCode = """import torch
    import torch.nn as nn

    def add(x,y):
        return x + y

    print("hel"""

    newPart = """lo world\")
    print(add(1,2))
    """

    context = SourceCodeCtx(sourceCode)
    for line in context.getLastLines(context.lineCount):
        print(line,end="")
    context.appendToContext(newPart)
    for line in context.getLastLines(context.lineCount):
        print(line,end="")
    print()
    print("*"*8)

    lineGen = context.reverseLineGen()
    for line in lineGen:
        print(line,end="")
    print()
    print("*"*40)
    print("Test Generate")
    print("*"*40)

def testGenerator():
    geneTool = Generator(Model("./tokenizer","./PyGen"),SourceCodeCtx(""))
    generatedLines = []
    while True:
        option = int(input("opt: 1->input new code 2->trager generate 3->confirm generate 4->list context:\n"))
        if option == 1:
            generatedLines = []
            newcode = input("new Code :with <N> denote newline and ENTER to submit\n>>>")
            geneTool.updateContext(newcode.replace("<N>","\n").splitlines(keepends=True))
        elif option == 2:
            generatedLines = geneTool.triggerGeneration(1)
            print("#"*40)
            for line in generatedLines:
                print(line)
            print("#"*40)
        elif option == 3:
            if not generatedLines == []:
                geneTool.affirmGeneration(generatedLines)
            generatedLines = []
        elif option == 4:
            print("#"*40)
            for line in geneTool._context.getLastLines(geneTool._context.lineCount):
                print(line,end="")
            print()
            print("#"*40)
        else:
            break

def testModel():
    model = Model("./tokenizer","./PyGen")
    print(model.encode("import torch.nn as nn"))
    print(len(model.encode("import torch.nn as nn")))
        
def main():
    testGenerator()

if __name__ == "__main__":
    main()
    
