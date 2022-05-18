#!/usr/bin/env python
from SourceCodeCtx import SourceCodeCtx

testlist = [1,2,3,4,5,6]
print(testlist[0:-1])

testlist = [ testlist[num - 1] for num in range(1,len(testlist) + 1)
        if num < 3 or num > 5]

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
