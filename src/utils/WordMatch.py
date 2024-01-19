import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

class WordMatch:
    """
    Tracking Keyword / Key header of interest in detected text
    """
    def __init__(self, layers=None):
        self.word_list = []
        self.layers = [-4, -3, -2, -1] if layers is None else layers
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        self.model = AutoModel.from_pretrained("bert-base-cased", output_hidden_states=True)

    # def get_word_idx(self, sent: str, word: str):
    #     return sent.split(" ").index(word)

    def get_hidden_states(self, encoded, token_ids_word, model, layers):
        """Push input IDs through model. Stack and sum `layers` (last four by default).
           Select only those subword token outputs that belong to our word of interest
           and average them."""
        with torch.no_grad():
            output = model(**encoded)

        # Get all hidden states
        states = output.hidden_states
        # Stack and sum all requested layers
        output = torch.stack([states[i] for i in layers]).sum(0).squeeze()
        # Only select the tokens that constitute the requested word
        word_tokens_output = output[token_ids_word]

        return word_tokens_output.mean(dim=0)

    def get_word_vector(self, sent, idx):
        """Get a word vector by first tokenizing the input sentence, getting all token idxs
           that make up the word of interest, and then `get_hidden_states`."""
        encoded = self.tokenizer.encode_plus(sent, return_tensors="pt")
        # get all token idxs that belong to the word of interest
        token_ids_word = np.where(np.array(encoded.word_ids()) == idx)

        return self.get_hidden_states(encoded, token_ids_word, self.model, self.layers)

    def add_keyword(self, word):
        if word not in self.word_list:
            self.word_list.append(word)
    def remove_keyword(self, word):
        if word in self.word_list:
            self.word_list.remove(word)
    def match_to_keyword(self, query_word, threshold=0.80):
        values = []
        max_score = 0
        matched_word = None
        for word in self.word_list:
            score = self.match(query_word, word)
            values.append(score)
            if score > max_score:
                max_score = score
                matched_word = word

        if max_score > threshold and matched_word is not None:
            return matched_word, score
        else:
            return None, None

    def word_embedding(self, words, idx=0):
        return self.get_word_vector(words, idx)

    def match(self, word1, word2):
        emb1 = self.word_embedding(word1)
        emb2 = self.word_embedding(word2)
        return self.cosine_similarity(emb1, emb2)

    def cosine_similarity(self, a, b, eps = 1e-08):
        denominator = max((np.linalg.norm(a) * np.linalg.norm(b)), eps)
        return np.dot(a, b) / denominator
