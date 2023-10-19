# CFComments

This repository contains the code as well the datasets associated with the task of predicting relevant and irrelevant comments to a blog post on Codeforces. The dataset contains 19 labelled comment threads(Dataset_educ_1.1.json contains 16 Educational Rounds, Dataset_div2_final contains 3 Div Rounds) and 1131 unlabelled comment threads(Dataset_unlabelled.json).

In the mlm folder, you can find the experiments associated with finetuning the models. 
In prompt generation folder you can find the input and output to be used by ChatGPT API(chatgpt_api_with_tree.py / chatgpt_api_without_tree.py) while in chatgpt_predictions you can find the results.

In order to run the experiments you need to pip install requirements.txt and pytorch. The finetuned models can be downloaded from https://drive.google.com/drive/folders/1X8PtijZw9y9FEhpPtlJUjQyjr-QyIj_d?usp=share_link.
