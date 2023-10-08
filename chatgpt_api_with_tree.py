import openai
import os
import time
from transformers import AutoTokenizer, OpenAIGPTDoubleHeadsModel

tokenizer = AutoTokenizer.from_pretrained("openai-gpt")

PROMPT_FOLDER = 'prompt_generation'
ROUND_TYPE = 'div'
ID = 2
with open(f'{PROMPT_FOLDER}/prompt_with_tree.txt', 'r') as fp:
    prompt = fp.read()

ROUND_FOLDER = f'{PROMPT_FOLDER}/{ROUND_TYPE}/{ID}'

trees_file_names = []

for file_name in os.listdir(ROUND_FOLDER):
    trees_file_names.append(file_name)

trees_file_names = sorted(trees_file_names)

from collections import defaultdict
round_trees = defaultdict(dict)

for fn in [file_name for file_name in trees_file_names]:
    root = fn.split('_')[0]
    type = fn.split('_')[1].split('.')[0]

    with open(f'{ROUND_FOLDER}/{fn}', 'r', encoding = 'utf-8') as fp:
        round_trees[root][type] = fp.read()


for root_id, tree in list(round_trees.items()):
    prediction_path = f'chatgpt_predictions/tree/{ROUND_TYPE}/{ID}'
    os.makedirs(prediction_path, exist_ok=True)
    with open(f'{prediction_path}/{root_id}_prediction.txt', 'w') as fp:
        text_part = tree['input']
        # prompt_num_tokens_length = len(tokenizer(prompt)['input_ids'])
        # text_part_num_tokens_length = len(tokenizer(text_part)['input_ids'])
        # total_tokens_length = prompt_num_tokens_length + text_part_num_tokens_length
        # if(total_tokens_length > 3900):
        #         print("Probably needs truncation")

        try:
            openai.api_key = "Your Key"
            response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            temperature = 0.2,
            max_tokens = 800,
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": '%rule%\n' + text_part},
            ]
            )
        except Exception as e:
            print(e)
            time.sleep(2)
            openai.api_key = "Your Key"
            response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            temperature = 0.2,
            max_tokens = 800,
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": '%rule%\n' + text_part},
            ]
            )


        result = response['choices'][0]['message']['content']

        fp.write(result)