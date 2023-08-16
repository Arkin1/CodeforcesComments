from embeddings_generation import TokenizedDataset, LayerEMBTokenEmbeddingGeneration
import os
import json
from collections import defaultdict
ROOT_PATH = "Assets/Embeddings"

def determine_tokens_statistics(textList:list[str], huggingface_bert_model_name):
    return TokenizedDataset(textList,huggingface_bert_model_name, device = "cpu").get_statistics()

def persist_embeddings(textList:list[str], huggingface_bert_model_name:str, alias:str, ids=None):
    dataset = TokenizedDataset(textList, huggingface_bert_model_name, truncation = True, max_length = 500)
    embeddings_per_layer = LayerEMBTokenEmbeddingGeneration(dataset).generate_embeddings()

    if(not os.path.exists(f"{ROOT_PATH}")):
        os.makedirs(f"{ROOT_PATH}")

    dict_embeddings = defaultdict(list)
    if(ids is None):
        ids = range(len(embeddings_per_layer))
    for id, v in zip(ids, embeddings_per_layer):
        dict_embeddings[id].append(v)

    with open(f"{ROOT_PATH}/{alias}.json", 'w') as fp:
        json.dump(dict_embeddings, fp)

def embedding_already_persisted(alias):
    return os.path.exists(f'{ROOT_PATH}/{alias}.json')

def load_embeddings(alias):
    with open(f'{ROOT_PATH}/{alias}.json', 'r') as fp:
        return json.load(fp)