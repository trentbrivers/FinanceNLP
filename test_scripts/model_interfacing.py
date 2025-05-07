from datasets import Dataset
from transformers import AutoModel, AutoTokenizer, DataCollatorWithPadding, TFAutoModelForSequenceClassification, create_optimizer
import numpy as np
import tensorflow as tf

checkpoint = r"E:\Data\NLP\Distilbert"

from preprocessing_inputs import process_input
id2label = {0: "Strong Sell", 1: "Sell", 2: "Hold", 3: "Buy", 4: "Strong Buy"}
label2id = {"Strong Sell": 0, "Sell": 1, "Hold": 2, "Buy": 3, "Strong Buy": 4}

test = "Volkswagen: Large Cost Savings Promised Without Factory Closures, We Remain Skeptical on Execution Analyst Note Rella Suskin, CFA, Equity Analyst, 23 Dec 2024 In line with expectations, no-moat Volkswagen ’ s agreement with labor will not result in factory closures in the company ’ s attempt to improve the competitiveness of the Volkswagen passenger cars, commercial vehicles, and group components divisions. This is the third unsuccessful attempt to structurally reduce capacity through plant closures in Volkswagen ’ s recent history. Despite this, Volkswagen will be reducing its production capacity in Germany by 734,000 units (8% of 2023 ’ s vehicle sales volume) and its German labor force by 35,000 (5% of total workforce) by 2030 to match Europe ’ s now structurally lower postpandemic annual demand for vehicles as well as to defend against intensifying Chinese competition. We are skeptical about the EUR 15 billion per year maintainable cost savings Volkswagen states that it can achieve with the terms of this agreement over the medium term. While the number of production lines per German plant will be reduced and simplified, the fixed costs associated with the running of each plant will need to be maintained. Volkswagen expects a short-term EUR 4 billion in cost savings associated with current restructurings. We forecast an immediate cost savings of EUR 2 billion per year in 2025, which can be maintained into the future. Given Volkswagen ’ s historically uninspiring execution track record, we maintain our fair value estimate at EUR 264 per share."

model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenized_test = tokenizer(test, return_tensors = "tf")

test_prediction = model.predict(tokenized_test).logits
y_pred = int(tf.math.argmax(test_prediction, axis=-1)[0])
print(model.config.id2label[y_pred])
