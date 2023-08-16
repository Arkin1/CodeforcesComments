import os
import json
from collections import defaultdict
ROOT_PATH = "Assets/Augmentation"

def persist_augmentations(aug_list:list[str], alias:str, ids=None):

    if(not os.path.exists(f"{ROOT_PATH}")):
        os.makedirs(f"{ROOT_PATH}")
    dict_textList = {}
    if(ids is None):
        ids = range(len(aug_list))
    for id, v in zip(ids, aug_list):
        dict_textList[id] = v

    with open(f"{ROOT_PATH}/{alias}.json", 'w') as fp:
        json.dump(dict_textList, fp)

def augmentations_already_persisted(alias):
    return os.path.exists(f'{ROOT_PATH}/{alias}.json')

def load_augmentations(alias):
    with open(f'{ROOT_PATH}/{alias}.json', 'r') as fp:
        return json.load(fp)
        
    
