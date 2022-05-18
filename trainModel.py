#!/usr/bin/env python
## 
from transformers import GPT2Config, GPT2Tokenizer
from transformers import DataCollatorForLanguageModeling
from datasets import load_dataset
from transformers import Trainer,TrainingArguments
from transformers import AutoModelForPreTraining,GPT2LMHeadModel

##

modelName = "PyGenSmall"
dataSetName = "./codeBaseSmall.txt"
modleDir = modelName
modleLogDir = modleDir + "Log"

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

# model = AutoModelForPreTraining.from_pretrained(pretrained_model_name_or_path = "PyGenNew/checkpoint-144000",config = config)
model = GPT2LMHeadModel(config)

paths = [dataSetName]
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
        output_dir= modleDir,
        logging_strategy="steps",
        logging_steps=100,
        logging_dir=modleLogDir,
        report_to="tensorboard",
        overwrite_output_dir=True,
        num_train_epochs=8,
        per_device_train_batch_size=3,
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

# trainer.train("./PyGenNew/checkpoint-144000")
trainer.train()
trainer.save_model(modleDir)

