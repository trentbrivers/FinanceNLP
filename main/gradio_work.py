import gradio as gr
from datasets import Dataset
from transformers import AutoModel, AutoTokenizer, DataCollatorWithPadding, TFAutoModelForSequenceClassification, create_optimizer
import numpy as np
import tensorflow as tf

checkpoint = r"E:\Data\NLP\Distilbert"

model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

def classification_prediction(user_text):
    tokenized_text = tokenizer(user_text, truncation = True, return_tensors = "tf")
    text_logit = model.predict(tokenized_text).logits
    text_prediction = int(tf.math.argmax(text_logit, axis=-1)[0])
    return model.config.id2label[text_prediction]


def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn = classification_prediction,
    inputs = ["text"],
    outputs = ["text"]
)

demo.launch()


