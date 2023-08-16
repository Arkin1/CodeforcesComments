from transformers import AutoModel, AutoTokenizer
from torch.utils.data.dataset import Dataset
from torch.utils.data.dataloader import DataLoader
from tqdm import tqdm

import pandas as pd
import torch
import numpy as np

class TokenizedDataset(Dataset):
    def __init__(self, textList:list[str],tokenizer_name:str, device:str = "cuda", **tokenizer_params):
        self.tokenizer_name = tokenizer_name
        self.tokenizer_params = tokenizer_params
        self.device = device
        self.textList = textList
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def __len__(self):
        return len(self.textList)

    def __getitem__(self, index):
        text = self.textList[index]
        tokenized_input  = self.tokenizer(text, **self.tokenizer_params, return_tensors = 'pt') 

        return {k:v[0].to(self.device) for k,v in tokenized_input.items()}
    def get_statistics(self):
        statistics = {"nrTokens":[], "nrWholeWords":[], "maxWordSplit":[], "nrWordsSplitAtleastTwice":[]}
        dataset = self
        
        for tokenized in dataset:
            input_ids = tokenized["input_ids"].tolist()
            statistics["nrTokens"].append(len(input_ids))

            nrWholeWords = 0
            maxWordSplit = 0
            nrWordsSplitAtleastTwice = 0
            last_input_id_position = -1
            for pos, input_id in enumerate(input_ids):
                conv_input_id = self.tokenizer.convert_ids_to_tokens(input_id)
                if(not conv_input_id.startswith("##")):
                    nrWholeWords+=1
                    if(pos - last_input_id_position - 1 > maxWordSplit):
                        maxWordSplit = pos - last_input_id_position - 1

                    if(pos - last_input_id_position - 1 > 0):
                        nrWordsSplitAtleastTwice+=1

                    last_input_id_position = pos

            statistics["nrWholeWords"].append(nrWholeWords)
            statistics["maxWordSplit"].append(maxWordSplit)
            statistics["nrWordsSplitAtleastTwice"].append(nrWordsSplitAtleastTwice)


        return pd.DataFrame(statistics)

    
class AbstractEmbeddingGeneration():
    def __init__(self, dataset:TokenizedDataset):
        self.dataset = dataset
        self.model = AutoModel.from_pretrained(dataset.tokenizer_name)
        self.model.to(self.dataset.device)
    
    def generate_embeddings(self) -> list[np.ndarray]:
        dataloader = DataLoader(self.dataset, 1)
        all_embeddings = []
        for tokenized_input in tqdm(dataloader):
            embeddings = self.model(output_hidden_states = True, **tokenized_input)
            layer_embeddings = []
            for layer in embeddings.hidden_states:
                layer = layer.detach().cpu().numpy()
                layer_embeddings.append(self.layer_aggregation_method(layer))
            all_embeddings.append(layer_embeddings)
        return all_embeddings

    def layer_aggregation_method(self, layer_hidden_state):
        pass

class LayerEMBTokenEmbeddingGeneration(AbstractEmbeddingGeneration):
    def __init__(self, dataset:TokenizedDataset):
        super().__init__(dataset)
    def layer_aggregation_method(self, layer_hidden_state:torch.Tensor):
        return layer_hidden_state[0,0].tolist()
    