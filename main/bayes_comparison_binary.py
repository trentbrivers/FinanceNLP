import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk import FreqDist, classify, ConfusionMatrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from tabulate import tabulate
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import seaborn as sns
import random
import evaluate

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
data_text = data_dict["text"]
data_all_tokenized = [word_tokenize(text) for text in data_text]

all_words = FreqDist(word.lower() for word in word_tokenize(" ".join(data_text)))
word_features = list(all_words)

def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains({})'.format(word)] = (word in document_words)
	return features

documents = list(zip(data_all_tokenized, data_dict["labels"]))

train_size = int(len(documents)*0.9)
train_set = [(document_features(doc), category) for (doc, category) in documents[:train_size]]
test_set = [(document_features(doc), category) for (doc, category) in documents[train_size:]]

classifier_Bayes = NaiveBayesClassifier.train(train_set)

test_actual = [label for (features,label) in test_set]
bayes_predicted = [classifier_Bayes.classify(features) for (features, label) in test_set]

bayes_accuracy = accuracy_score(test_actual,bayes_predicted)
bayes_precision = precision_score(test_actual,bayes_predicted, average= None)
bayes_recall = recall_score(test_actual, bayes_predicted, average = None)

results_table = tabulate([['Bayes', bayes_accuracy,bayes_precision,bayes_recall]],
	headers = ['Model', 'Accuracy', 'Precision', 'Recall'])

print(results_table)
confusion_metric = evaluate.load("confusion_matrix")
cm_computed = confusion_metric.compute(references = test_actual, predictions = bayes_predicted)
cm = cm_computed["confusion_matrix"]

labels = ['Sell','Buy']

sns.heatmap(cm, annot=True, fmt="d", cmap="Reds", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.savefig(r"C:\Users\trent\Dropbox\Education Docs\2025 Spring - CSPB 4830 - Natural Language Processing\NLP_Project\FinanceNLP\bayes_performance_binary.png")