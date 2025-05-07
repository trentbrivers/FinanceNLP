from datasets import Dataset
from transformers import AutoModel, AutoTokenizer, DataCollatorWithPadding, TFAutoModelForSequenceClassification, create_optimizer
import numpy as np
import evaluate
import tensorflow as tf

checkpoint = "distilbert/distilbert-base-uncased" #First working checkpoint
#checkpoint = "allenai/longformer-base-4096" #The first test will be with longformer-base-4096
#checkpoint = "openai-community/gpt2"

# id2label = {1: "Strong Sell", 2: "Sell", 3: "Hold", 4: "Buy", 5: "Strong Buy"}
# label2id = {"Strong Sell": 1, "Sell": 2, "Hold": 3, "Buy": 4, "Strong Buy": 5}

#labels for distilbert
# id2label = {0: "Strong Sell", 1: "Sell", 2: "Hold", 3: "Buy", 4: "Strong Buy"}
# label2id = {"Strong Sell": 0, "Sell": 1, "Hold": 2, "Buy": 3, "Strong Buy": 4}
id2label = {0: "Sell", 1: "Buy"}
label2id = {"Sell": 0, "Buy": 1}

def load_data_to_dict(raw_data):
	"""takes in a list of strings and parses them to a data dictionary"""
	data_dict = {"text": [], "labels": []}
	for text_data_label in raw_data:
		text_data_label = text_data_label.rstrip()
		data_dict["text"].append(text_data_label[:-1])
		data_dict["labels"].append(0 if int(text_data_label[-1])-1 <= 2 else 1)

	return data_dict

#Create a Huggingface dataset from the compiled data
datafile = open("morningstar_data.txt", "r", encoding="utf-8")
all_text = datafile.readlines()
datafile.close()

#Step 1: Load a Dataset
data_dict = load_data_to_dict(all_text)
ds = Dataset.from_dict(data_dict)

#Step 2: Preprocess the Data
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
#tokenizer.add_special_tokens({'pad_token': '[PAD]'})

def preprocess_fuction(data):
	return tokenizer(data["text"], truncation = True, max_length = 512, padding = "max_length")

data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors ="tf")

tokenized_data = ds.map(preprocess_fuction, batched = True)
split_set = tokenized_data.train_test_split(test_size=0.1, seed = 42)


model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels = 2, id2label = id2label, label2id = label2id)

tf_train_set = model.prepare_tf_dataset(
	split_set["train"],
	shuffle = False,
	batch_size = 8, 
	collate_fn = data_collator
)

#I'm going to attempt to train it without a validation set split first. 
tf_test_set = model.prepare_tf_dataset(
	split_set["test"],
	shuffle = False,
	batch_size = 8,
	collate_fn = data_collator
)

#Step 3: Let's get ready to train
batch_size = 8
num_epochs = 5
batches_per_epoch = len(split_set["train"])
total_train_steps = int(batches_per_epoch * num_epochs)
optimizer, schedule = create_optimizer(init_lr=2e-5, num_warmup_steps=0, num_train_steps = total_train_steps)

model.compile(optimizer=optimizer, metrics = ["accuracy"])

model.fit(x=tf_train_set, epochs = num_epochs)

model.save_pretrained(r"E:\Data\NLP")
tokenizer.save_pretrained(r"E:\Data\NLP")

#print(split_set)
# test_text = ds[0]["text"]
# test_text = test_text*2
# test = tokenizer(test_text, truncation = True, max_length = 4096, padding = "max_length")
# print(test, len(test[0]))

