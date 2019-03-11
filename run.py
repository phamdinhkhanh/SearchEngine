from core_nlp.tokenization.base_tokenizer import BaseTokenizer
from core_nlp.tokenization.utils import load_n_grams
import os
import pandas as pd

__author__ = "Ha Cao Thanh"
__copyright__ = "Copyright 2018, DeepAI-Solutions"


class LongMatchingTokenizer(BaseTokenizer):
    def __init__(self, bi_grams_path='bi_grams.txt', tri_grams_path='tri_grams.txt', four_grams_path='four_grams.txt'):
        """
        Initial config
        :param bi_grams_path: path to bi-grams set
        :param tri_grams_path: path to tri-grams set
        """
        self.bi_grams = load_n_grams(bi_grams_path)
        self.tri_grams = load_n_grams(tri_grams_path)
        self.four_grams = load_n_grams(four_grams_path)

    def tokenize(self, text):
        """
        Tokenize text using long-matching algorithm
        :param text: input text
        :return: tokens
        """
        syllables = LongMatchingTokenizer.syllablize(text)
        # print('syllables:', syllables)
        syl_len = len(syllables)
        curr_id = 0
        word_list = []
        done = False
        while (curr_id < syl_len) and (not done):
            # print('word_list: ',word_list, '\n')
            # print('syllables: ', syllables)
            curr_word = syllables[curr_id]
            if syl_len == 3:
                done = True
                next_word = syllables[curr_id + 1]
                next_next_word = syllables[curr_id + 2]
                pair_word = ' '.join([curr_word.lower(), next_word.lower()])
                triple_word = ' '.join([curr_word.lower(), next_word.lower(), next_next_word.lower()])
                if triple_word in self.tri_grams:
                    word_list.append('_'.join([curr_word, next_word, next_next_word]))
                elif pair_word in self.bi_grams:
                    word_list.append('_'.join([curr_word, next_word]))
                else:
                    word_list.append(curr_word)
            elif syl_len == 2:
                done = True
                next_word = syllables[curr_id + 1]
                pair_word = ' '.join([curr_word.lower(), next_word.lower()])
                if pair_word in self.bi_grams:
                    word_list.append('_'.join([curr_word, next_word]))
                else:
                    word_list.append(curr_word)
            elif syl_len == 1:
                done = True
                word_list.append(curr_word)
            elif curr_id <= (syl_len - 3):
                next_word = syllables[curr_id + 1]
                next_next_word = syllables[curr_id + 2]
                pair_word = ' '.join([curr_word.lower(), next_word.lower()])
                triple_word = ' '.join([curr_word.lower(), next_word.lower(), next_next_word.lower()])
                if triple_word in self.tri_grams:
                    word_list.append('_'.join([curr_word, next_word, next_next_word]))
                    curr_id += 3
                elif pair_word in self.bi_grams:
                    word_list.append('_'.join([curr_word, next_word]))
                    curr_id += 2
                else:
                    word_list.append(curr_word)
                    curr_id += 1
            elif curr_id <= (syl_len - 2):
                next_word = syllables[curr_id + 1]
                pair_word = ' '.join([curr_word.lower(), next_word.lower()])
                if pair_word in self.bi_grams:
                    word_list.append('_'.join([curr_word, next_word]))
                    curr_id += 2
                else:
                    word_list.append(curr_word)
                    word_list.append(next_word)
                    curr_id += 2
            else: done = True
        return word_list


"""Tests"""


def test():
    lm_tokenizer = LongMatchingTokenizer()
    tokens = lm_tokenizer.tokenize('Pin điện thoại iPhone 6')
    print(tokens)
    # return tokens


if __name__ == '__main__':
    os.chdir('./core_nlp/tokenization')
    dataset = pd.read_excel('SearchItems.xlsx',sheet_name = 'Sheet1', header = 0, encoding = 'ISO-8859-1', names = ['Term', 'Frequence'])
    dics = []
    for term in dataset.Term.tolist():
        lm_tokenizer = LongMatchingTokenizer()
        tokens = lm_tokenizer.tokenize(term)
        dics.append(tokens)
    dataset['Tokenizer'] = dics
    dataset.to_csv('SearchItems.csv')
    # test()
