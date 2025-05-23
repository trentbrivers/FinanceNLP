# FinanceNLP
A project to experiment with fine-tuning pre-trained transformers to conduct textual classification with the 5 stock analyst ratings.

library dependencies: numpy, tensorflow, transformers, evaluate, datasets, pypdf, matplotlib, seaborn, gradio, nltk

The main files necessary to run this project are located in the 'main' folder. Since the full Morningstar reports are copyrighted, I can not redistribute them, but the processed .txt file of my data will be maintained until that needs to change. 
If you do find yourself in possession of a folder on your hard drive full of Morningstar equity reports, then open the consolidate_processed_data.py script, change the 'path' variable to the correct path to your folder, and then run the script. This script calls the process_input function from my preprocessing_inputs.py script, which uses regular expressions to parse the PDF files into the relevant sections. consolidate_processed_data.py will create a morningstar_data.txt data in your folder.

After you have the morningstar_data.txt file created by consolidate_processed_data.py, open main_file.py. main_file.py needs to be located in the same directory folder as morningstar_data.txt. You can change the 'checkpoint' variable to any HuggingFace model you wish to train for textual classification. main_file.py is where we are going to train our model. Feel free to change the hyperparameters as you see fit; however, you will want to change the paths at line 78 and line 79 to save the model and tokenizer to the proper locations of your choosing. It is worth noting here that predetermined seed values were used to split the training and testing sets. These can be changed if you want, but do remember what value you used (if you did use one) because you'll need that value later for evaluation. 

Once you have the trained model saved on your drive, there are a couple of options for you. The first is to evaluate the performance of the model. This can be done with model_evaluation.py. Change the checkpoint to the correct directory where your model is located. If you used a seed value for the train/test split during training, input that at line 46, where you see 'seed'. Running this script will output two files: a .txt file with the accuracy, f1, precision, and recall of your trained model, and the confusion matrix of the predictions of your model. 

If you wish to interface with the trained model, then run gradio_work.py! You can input text to the trained model from the interface, and it will present you with a rating based on the text. 

There are other scripts present in main, but these are only helpful for understanding and contextualizing the results of this project. Run them if you want to. bayes_comparison.py creates a naive Bayes classifier with five labels and tests its classification performance. The only thing you'll want to change there is the path on line 72. The same is true for bayes_comparison_binary.py. test_binary_classification.py and binary_model_evaluation.py are essentially the same as main_file.py and model_evaluation.py, so whatever changes were recommended to those files also apply here. 

Within the main folder, you will see the evaluation folder. This holds all of the output metrics in the eval.txt files and the confusion matrices for the created models. 

You can ignore the test_scripts folder (unless you're curious). Everything present in there is just a bunch of code sketches, tests, and experiments performed in order to get everything else working.
