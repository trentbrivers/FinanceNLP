import matplotlib.pyplot as plt
import numpy as np

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

id2label = {0: "Strong Sell", 1: "Sell", 2: "Hold", 3: "Buy", 4: "Strong Buy"}

data_dict = load_data_to_dict(all_text)
only_labels = data_dict["labels"]
unique, counts = np.unique(only_labels, return_counts = True)
#print(dict(zip(unique, counts)))
mapping = [id2label[item] for item in unique]

label_count = dict(zip(mapping, counts))
print(label_count)

plt.figure()
plt.bar(label_count.keys(), label_count.values())
plt.title("Label Distribution")
plt.xlabel("Label")
plt.ylabel("Count")
plt.savefig(r"C:\Users\trent\Dropbox\Education Docs\2025 Spring - CSPB 4830 - Natural Language Processing\NLP_Project\FinanceNLP\data_distribution.png")

plt.figure()
data_total = len(only_labels)
percentage = [count / data_total for count in counts]
plt.bar(label_count.keys(), percentage, color='red')
plt.title("Label Distribution")
plt.xlabel("Label")
plt.ylabel("Percent of Total")
plt.savefig(r"C:\Users\trent\Dropbox\Education Docs\2025 Spring - CSPB 4830 - Natural Language Processing\NLP_Project\FinanceNLP\data_distribution_percent.png")
