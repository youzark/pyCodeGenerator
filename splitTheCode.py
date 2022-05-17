#!/usr/bin/env python
import os

def splitFileIntoSmallDataSet(filename,newFileName,sizeInMByte):
    sizeLength = sizeInMByte * 1024 * 1024
    with open(filename,"r") as f:
        content = ""
        while len(content) < sizeLength:
            content += f.readline()
    with open(newFileName,"w") as wf:
        wf.write(content)

def main():
    splitFileIntoSmallDataSet("./pythonNewCodeBase.txt","codeBaseSmall.txt",30)
    splitFileIntoSmallDataSet("./pythonNewCodeBase.txt","codeBaseMedium.txt",80)

if __name__ == "__main__":
    main()
