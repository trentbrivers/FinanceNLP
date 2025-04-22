from datasets import Dataset
from transformers import AutoModel, AutoTokenizer, DataCollatorWithPadding, TFAutoModelForSequenceClassification, create_optimizer
import numpy as np
import evaluate
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import os

checkpoint = r"E:\Data\NLP\Longformer"
id2label = {0: "Strong Sell", 1: "Sell", 2: "Hold", 3: "Buy", 4: "Strong Buy"}
label2id = {"Strong Sell": 0, "Sell": 1, "Hold": 2, "Buy": 3, "Strong Buy": 4}

model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels = 5, id2label = id2label, label2id = label2id)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

def load_data_to_dict(raw_data):
	"""takes in a list of strings and parses them to a data dictionary"""
	data_dict = {"text": [], "labels": []}
	for text_data_label in raw_data:
		text_data_label = text_data_label.rstrip()
		data_dict["text"].append(text_data_label[:-1])
		data_dict["labels"].append(int(text_data_label[-1])-1)

	return data_dict

#Create a Huggingface dataset from the compiled data
datafile = open("morningstar_data.txt", "r", encoding="utf-8")
all_text = datafile.readlines()
datafile.close()

#Step 1: Load a Dataset
data_dict = load_data_to_dict(all_text)
ds = Dataset.from_dict(data_dict)

#Step 2: Preprocess the Data
# tokenizer = AutoTokenizer.from_pretrained(checkpoint)
#tokenizer.add_special_tokens({'pad_token': '[PAD]'})

def preprocess_fuction(data):
	return tokenizer(data["text"], truncation = True, max_length = 1024, padding = "max_length")

data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors ="tf")

tokenized_data = ds.map(preprocess_fuction, batched = True)
split_set = tokenized_data.train_test_split(test_size=0.1, seed = 84)

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

#Evaluate
predictions = model.predict(tf_test_set).logits
y_pred = np.argmax(predictions, axis=1)

# Get the true labels
y_true = np.concatenate([y for x, y in tf_test_set], axis=0)

accuracy = evaluate.load("accuracy")
f1 = evaluate.load("f1")
precision = evaluate.load("precision")
recall = evaluate.load("recall")
confusion_matrix = evaluate.load("confusion_matrix")

results = {
    "accuracy": accuracy.compute(predictions=y_pred, references=y_true),
    "f1": f1.compute(predictions=y_pred, references=y_true, average="weighted"),
    "precision": precision.compute(predictions=y_pred, references=y_true, average="weighted"),
    "recall": recall.compute(predictions=y_pred, references=y_true, average="weighted"),
    "confusion_matrix": confusion_matrix.compute(predictions=y_pred, references=y_true, labels = list(range(5))),
}

for metric_name, metric_result in results.items():
    print(f"{metric_name}: {metric_result}")

cm = results["confusion_matrix"]["confusion_matrix"]
labels = ['Strong Sell', 'Sell', 'Hold', 'Buy', 'Strong Buy']

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.savefig(os.path.join(checkpoint, 'confusion_matrix.png'))


with open(os.path.join(checkpoint, "eval_file.txt"), "w", encoding="utf-8") as file:
	#format: each line has two components: the information as a long string, and the last character being the label
	for metric_name, metric_result in results.items():
		file.write(metric_name + ": " + str(metric_result) + "\n")