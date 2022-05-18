#!/usr/bin/env python
from transformers import GPT2Tokenizer
from transformers import GPT2LMHeadModel

class Model:
    def __init__(self,tokenizerDir : str,modelDir : str,device = "cuda"):
        self.tokenizer = self._loadGPT2Tokenizer(tokenizerDir)
        self.model = self._loadGPT2Model(modelDir)
        self._device = device

    def _loadGPT2Tokenizer(self,tokenizerDir):
        tokenizer = GPT2Tokenizer.from_pretrained(tokenizerDir)
        tokenizer.add_special_tokens({
            "eos_token": "</s>",
            "bos_token": "<s>",
            "unk_token": "<unk>",
            "pad_token": "<pad>",
            "mask_token": "<mask>"
            })
        return tokenizer

    def _loadGPT2Model(self,modelDir):
        model = GPT2LMHeadModel.from_pretrained(modelDir).to(self._device)
        return model

    def _decodeNewLine(self,codeSnippet : str) -> str:
        return codeSnippet.replace("<N>","\n")

    def _encodeNewLine(self,codeSnippet : str) -> str:
        return codeSnippet.replace("\n","<N>")

    def generateCodeSnippet(self,context,maxLength,beams = 3,temperature = 0.7) -> str:
        inputIDs = self.encode(self._encodeNewLine(context))
        modelOutput = self.model.generate(
                inputIDs,
                max_length = maxLength,
                num_beams = beams,
                temperature = temperature,
                no_repeat_ngram_size = 5,
                num_return_sequences = 1
                )
        return self._decodeNewLine(self.decode(modelOutput[0]))

    def encode(self,codeSnippet : str):
        return self.tokenizer.encode(codeSnippet,return_tensors="pt").to(self._device)

    def decode(self,tokens):
        return self.tokenizer.decode(tokens)
