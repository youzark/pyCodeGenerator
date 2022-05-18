#!/usr/bin/env python
from generator.Generator import Generator
from generator.Model import Model
from generator.SourceCodeCtx import SourceCodeCtx
import random 
import ast


def makeEvaluateSet():
    with open("./evaluateSet.txt","r") as f:
        codeSnippets = f.read().splitlines(keepends=False)
        
    for codeSnippet in codeSnippets:
        codeSnippet = codeSnippet.replace("<N>","\n")
        pickLineNum = random.randint(5,15)
        codeLines = codeSnippet.splitlines(keepends=True)[0:pickLineNum]
        codeSnippet = "".join(codeLines)
        if parsable(codeSnippet):
            yield "".join(codeLines)

def parsable(codeSnippet) -> bool:
    try:
        ast.parse(codeSnippet)
    except:
        return False
    return True

def doSingleEva(evaData:str,generator:Generator):
    generator.recreateCtx(evaData)
    return parsable("".join(generator.triggerGeneration(10)))

def main():
    modelDir = "./PyGen"
    tokenizerDir = "./tokenizer"
    generator = Generator(Model(tokenizerDir=tokenizerDir,modelDir=modelDir),SourceCodeCtx(""))
    evaluateSet = makeEvaluateSet()
    evaCount = 0
    passCount = 0

if __name__ == "__main__":
    main()
