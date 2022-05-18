#!/usr/bin/env python

class SourceCodeCtx():
    def __init__(self,sourceCode : str):
        self._source = sourceCode
        self._lines = []
        self._parse()

    def _parse(self):
        self._lines = self._source.splitlines(keepends=True)
        self.lineCount = len(self._lines)

    def _concate(self):
        self._source = "".join(self._lines)
        self.lineCount = len(self._lines)

    def getLastLines(self,lineCount : int) -> list[str]:
        """
        return last {lineCount} lines in the context,if the last line is not finished with "\n" , it will still count as a single line as long as it's not empty.
        """
        return self._lines[-lineCount:]

    def reverseLineGen(self):
        for line in self._lines[-1::-1]:
            yield line

    def appendToContext(self,codeSnippet : str):
        """
        append new code to the back of context
        """
        self._source += codeSnippet
        self._parse()

    def removeLines(self,startLineNum : int,endLineNum : int) -> list[str]:
        """
        remove all lines from startLineNum to endLineNum( start from 0 )
        the removed lines will be returned in list
        """
        removedLines = self._lines[startLineNum:endLineNum+1]
        self._lines = [ self._lines[lineNumber] 
                for lineNumber in range(0,len(self._lines))
                if lineNumber < startLineNum or lineNumber > endLineNum]
        self._concate()
        return removedLines
