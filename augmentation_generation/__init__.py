from numpy import random
import nlpaug.augmenter.word as waug
from tqdm import tqdm

class WeakAugmenter:
    def __init__(self, p_drop=0.1, p_syn=0.1, p_swap=0.1, p_capitalize=0.1, max_no_capitalization=3):
        self.p_drop = p_drop
        self.p_syn = p_syn
        self.p_swap = p_swap
        self.p_capitalize = p_capitalize
        self.max_no_capitalization = max_no_capitalization
        self.drop_aug = waug.RandomWordAug(action="delete", aug_p=self.p_drop)
        self.syn_aug = waug.SynonymAug(aug_p=self.p_syn)
        self.swap_aug = waug.RandomWordAug(action="swap", aug_p=self.p_swap)

    def augment(self, text):
        # Apply dropout augmentation
        if random.uniform(0, 1) < self.p_drop:
            text = self.drop_aug.augment(text)
            if isinstance(text, list):
              if len(text) != 0:
                text = text[0]

        # Apply synonym replacement augmentation
        if random.uniform(0, 1) < self.p_syn:
            text = self.syn_aug.augment(text)
            if isinstance(text, list):
              if len(text) != 0:
                text = text[0]

        # Apply random swapping augmentation
        if random.uniform(0, 1) < self.p_swap:
            text = self.swap_aug.augment(text)
            if isinstance(text, list):
              if len(text) != 0:
                text = text[0]
        
        if (random.uniform(0, 1) < self.p_capitalize):
            splitted_text = text.split(' ')
            pos_capitalizations = random.randint(low=0, high= len(splitted_text),
                                                size=(self.max_no_capitalization))
            for random_pos in pos_capitalizations:
              if(len(splitted_text[random_pos]) > 1):
                splitted_text[random_pos] = str.upper(splitted_text[random_pos][0]) + splitted_text[random_pos][1:]
              else:
                splitted_text[random_pos] = str.upper(splitted_text[random_pos])
        return text

def get_weak_augmented_text(text_list, number_samples = 10, **kwargs):
  #augmenter = WeakAugmenter(0.25, 0.33, 0.4, 0.5, 3)
  augmenter = WeakAugmenter(**kwargs)
  augmented_text_list = []
  for text in tqdm(text_list):
    augmented_samples = []
    for i in range(number_samples):
      augmented_text = augmenter.augment(text)
      if isinstance(augmented_text, list):
        if len(augmented_text) != 0:
          augmented_text = augmented_text[0]

          augmented_samples.append(augmented_text)
      else:
        augmented_samples.append(augmented_text)
    augmented_text_list.append(augmented_samples)
  
  return augmented_text_list