#!/usr/bin/env python
from SourceCodeCtx import SourceCodeCtx
from Model import Model

class Generator:
    def __init__(self,model : Model,sourceCodeCtx : SourceCodeCtx):
        self._model = model
        self._context = sourceCodeCtx

    def triggerGeneration(self,lineNum : int) -> list[str]:
        """
        generate lines of code with current CodeContext
        lines will be returned in a List as string without trailing \n
        unfinished last line of code will be filled and count as a line But only the generated part will be returned
        """
        estimateTokensPerLine = 30
        context = self.getContextGivenTokenLimit(400)
        maxLength = min(1024,self._model.countTokens(context) + lineNum * estimateTokensPerLine)
        generatedCodeSnippet = self._model.generateCodeSnippet(context=context,maxLength=maxLength)
        generatedLines = generatedCodeSnippet.splitlines(keepends=True)
        if len(generatedCodeSnippet) <= lineNum:
            return generatedLines[0:-1]
        return generatedLines[0:lineNum]

    def getContextGivenTokenLimit(self,tokenLimit):
        lineGen = self._context.reverseLineGen()
        tokens = 0
        context = ""
        for line in lineGen:
            context = line + context
            tokens += self._model.countTokens(line)
            if tokens > tokenLimit:
                return context
        return context

    def updateContext(self,newLines : list[str]):
        self._context.appendToContext("".join(newLines))

    def affirmGeneration(self,newLines : list[str]):
        self.updateContext(newLines)
