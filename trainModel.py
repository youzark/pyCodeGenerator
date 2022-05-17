#!/usr/bin/env python
## 
from transformers import GPT2Config, GPT2Tokenizer
from transformers import DataCollatorForLanguageModeling
from datasets import load_dataset
from transformers import Trainer,TrainingArguments
from transformers import AutoModel
##

def loadGPT2Tokenizer():
    tokenizer = GPT2Tokenizer.from_pretrained("./tokenizer")
    tokenizer.add_special_tokens({
        "eos_token": "</s>",
        "bos_token": "<s>",
        "unk_token": "<unk>",
        "pad_token": "<pad>",
        "mask_token": "<mask>"
        })
    return tokenizer

tokenizer = loadGPT2Tokenizer()
config = GPT2Config(
        vocab_size= tokenizer.vocab_size,
        bos_token = tokenizer.bos_token_id,
        eos_token = tokenizer.eos_token_id
        )

model = AutoModel.from_pretrained(pretrained_model_name_or_path = "./PyGen/",config = config)

paths = ["./pythonCodeBase.txt"]
dataset = load_dataset("text",data_files=paths)

def encode(lines):
    return tokenizer(lines["text"],
            add_special_tokens=True,
            truncation=True,
            max_length=1024)

dataset.set_transform(encode)
dataset = dataset["train"]
dataCollator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=True,
        mlm_probability=0.15)

trainingArgs = TrainingArguments(
        output_dir= "PyGen",
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_device_train_batch_size=8,
        save_steps=2_000,
        save_total_limit=2,
        prediction_loss_only=True,
        remove_unused_columns=False,
        )

trainer = Trainer(
        model = model,
        args = trainingArgs,
        data_collator = dataCollator,
        train_dataset = dataset,
        )

trainer.train()
trainer.save_model("./PyGen")
