### Messages from Ray:
### 1. I've done the testing with the AdamSavage_2008P.txt file in this folder.
###    The current version is still using the file path to read files. 
###    if any adjustments are needed, refer to the __init__ part of the class, the file should be taken as a input of the class initialization.
###
### 2. installing en_core_web_sm can take a while. And you might run into a weird error that says: 
###    OMP: Error #15: Initializing libiomp5.dylib, but found libomp.dylib already initialized.
###    Try this if you encounter this problem: 
###        1. conda install nomkl
###        2. python -m spacy download en
###
### 3. Comments are mostly written by me (Ray), which I am not very sure if I 100% understood the code correctly >_<'''
###    Feel free to edit the comments :)
###
### 4. There is a sample output below, it seems like the function_R is missing? I'm not quite sure about it, I'll check with 宸宇

import nltk
import spacy
import en_core_web_sm
import spacy
from negspacy.negation import Negex
import pandas as pd
import numpy as np
import csv
from spacy.matcher import PhraseMatcher
from negspacy.termsets import termset
from negspacy.negation import Negex

class NLP_features():
    # Global attributes
    nlp = en_core_web_sm.load()
    nlp = spacy.load("en_core_web_sm")

    def __init__(self, file_handler):
        self.file_handler = open(file_handler, "r")
        self.word_dict = {}
        self.feature_table = np.zeros(57)
        self.words = 0

    def doclen(self, line1):
        ''' Analyzes the basic part of speech in the transript fed. The analyzation works line by line.
            Input: A Sentence.
            Output: 
        '''
        doc = NLP_features.nlp(line1)
        return len(doc)
    
    def words_recognize(self, line1):
        ''' Partition of each part of speech in the transript fed. The analyzation works line by line.
            Input: A Sentence.
            Output: Dictionary with part of speech as the key, list of words as the value -> {part of speech : [list of words]}
        '''
        doc = NLP_features.nlp(line1)
        # part of speech given
        word_dic={}
        pos_tag=['SPACE','ADV','VERB','ADP','DET','NOUN','ADJ','PUNCT','INTJ','NUM','PRON','AUX','CCONJ','PART','PROPN','SCONJ','X','CONJ','SYM']
        for tag in pos_tag:
            list1=[]
            word_dic.update({tag:list1})
        for token in doc:
            word_dic[token.pos_].append(token.text)
        return word_dic
    def counting_lemma(self, line1):
        ''' Counts the number of lemmas in a sentence. 
            Input: a Sentence
            Output: 
        '''
        lemma_dict={}
        doc = NLP_features.nlp(line1)
        # Count token 
        for token in doc:
            if(token.lemma_ not in lemma_dict):
                lemma_dict.update({token.lemma_:1})
            else:
                lemma_dict[token.lemma_]+=1
        sort_dict=dict(sorted(lemma_dict.items(), key=lambda item: item[1]))

        max_freq =- 1
        most_freq_words = "none"
        for item in sort_dict:
            if(sort_dict[item]>max_freq and item!='.' or item!=','):
                max_freq=sort_dict[item]
            most_freq_words=item

        return len(lemma_dict), max_freq
    
    def counting_numnchunk(self, line1):
        ''' Count the total number of nouns in a sentence
            Input: A Sentence.
            Output: total nouns in the sentence.
        '''
        num = 0
        doc = NLP_features.nlp(line1)
        for chunk in doc.noun_chunks:
            num+=1
        return num
    
    def first_person_singular_verbs(self, line1):
        ''' Count the total number of first person singular verbs in a sentence
            Input: A sentence.
            Output: total number of first person singular verbs.
        '''
        doc = NLP_features.nlp(line1)
        singular_verbs = 0
        for i in range(0,len(doc)):
            if(doc[i].pos_=="VERB"):
                if(i>=1 and doc[i-1].text=="I"):
                    singular_verbs+=1
        return singular_verbs

    def mis_spell(self, line1):
        ''' Count the total number of misspelled words in a sentence
            Input: A sentence.
            Output: total number of misspelled words
        '''
        doc = NLP_features.nlp(line1)
        propn=[]
        propnum=0
        x_word=0

        for token in doc:
            if(token.pos_=="PROPN"):
                propnum+=1
            propn.append(token.text)

        for token in doc:
            if(token.pos_=="X" or token.pos_=="SYM"):
                x_word+=1

        real_propn=0
        for ent in doc.ents:
            if(ent.text in propn):
                real_propn+=1
        
        return propnum + x_word-real_propn

    def NES(self, line1):
        ''' Count the absolute time term in a sentence.
            Input: Sentence
            Output: Count of absolute time term.
        '''
        doc = NLP_features.nlp(line1)
        time_term=0
        term=0
        for ent in doc.ents:
            if(ent.label_=="TIME"):
                time_term+=1
            term+=1
        return time_term,term
    
    def neg_analyze(self, line1):
        ''' Find the number of negation words in a sentence
            Input: Sentence
            Output: Number of negation words
        '''
        doc = NLP_features.nlp(line1)
        negnum=0
        for e in doc.ents:
            negnum+=1
        return negnum
    
    def content_function(self, line1):
        ''' 虛實詞
            Input: Sentence
            Output: 
        '''
        doc = NLP_features.nlp(line1)
        content_num=0
        content_exception=["no", "not", "never", "this", "that", "these" ,"those","what", "where", "when", "how" , "why"]
        for token in doc:
            if(token.pos_=="NOUN"or token.pos_=="VERB" or token.pos_=="ADJ" or token.pos_=="ADV"):
                content_num+=1
            else:
                if(token.text in content_exception):
                    content_num+=1
        function_word=0
        for token in doc:
            if(token.pos_=="AUX" or token.pos_=="ADP" or token.pos_=="DET" or token.pos_=="CONJ" or token.pos_=="CCONJ" or token.pos_=="SCONJ" or token.pos_=="PRON"):
                if(token.text not in content_exception):
                    function_word+=1
        return content_num, function_word

    def generate_features(self):
        # Convert transcritps into features
        line1 = self.file_handler.readline()
        self.words = self.doclen(line1)
        self.word_dict = self.words_recognize(line1)
        self.feature_table[0]= self.words
        self.feature_table[1]=len(self.word_dict["SPACE"])
        self.feature_table[2]=len(self.word_dict["ADV"])
        self.feature_table[3]=len(self.word_dict["VERB"])
        self.feature_table[4]=len(self.word_dict["ADP"])
        self.feature_table[5]=len(self.word_dict["DET"])
        self.feature_table[6]=len(self.word_dict["NOUN"])
        self.feature_table[7]=len(self.word_dict["ADJ"])
        self.feature_table[8]=len(self.word_dict["PUNCT"])
        self.feature_table[9]=len(self.word_dict["INTJ"])
        self.feature_table[10]=len(self.word_dict["NUM"])
        self.feature_table[11]=len(self.word_dict["PRON"])
        self.feature_table[12]=len(self.word_dict["AUX"])
        self.feature_table[13]=len(self.word_dict["CCONJ"])
        self.feature_table[14]=len(self.word_dict["PART"])
        self.feature_table[15]=len(self.word_dict["PROPN"])
        self.feature_table[16]=len(self.word_dict["SCONJ"])
        self.feature_table[17]=len(self.word_dict["CONJ"])
        self.feature_table[18]=len(self.word_dict["PUNCT"])
        self.feature_table[19]=len(self.word_dict["INTJ"])
        self.feature_table[20],self.feature_table[21] = self.counting_lemma(line1)
        self.feature_table[22] = self.counting_numnchunk(line1)
        self.feature_table[23] = self.first_person_singular_verbs(line1)
        self.feature_table[24] = self.mis_spell(line1)
        self.feature_table[25],self.feature_table[26] = self.NES(line1)
        self.feature_table[27]= len(line1.split('.'))
        self.feature_table[28] = self.neg_analyze(line1)
        self.feature_table[29],self.feature_table[30] = self.content_function(line1)
        self.feature_table[31]=len(self.word_dict["SPACE"]) / self.words
        self.feature_table[32]=len(self.word_dict["ADV"]) / self.words
        self.feature_table[33]=len(self.word_dict["VERB"]) / self.words
        self.feature_table[34]=len(self.word_dict["ADP"]) / self.words
        self.feature_table[35]=len(self.word_dict["DET"]) / self.words
        self.feature_table[36]=len(self.word_dict["NOUN"]) / self.words
        self.feature_table[37]=len(self.word_dict["ADJ"]) / self.words
        self.feature_table[38]=len(self.word_dict["PUNCT"]) / self.words
        self.feature_table[39]=len(self.word_dict["INTJ"])/ self.words
        self.feature_table[40]=len(self.word_dict["NUM"]) / self.words
        self.feature_table[41]=len(self.word_dict["PRON"]) / self.words
        self.feature_table[42]=len(self.word_dict["AUX"]) / self.words
        self.feature_table[43]=len(self.word_dict["CCONJ"]) / self.words
        self.feature_table[44]=len(self.word_dict["PART"]) / self.words
        self.feature_table[45]=len(self.word_dict["PROPN"]) / self.words
        self.feature_table[46]=len(self.word_dict["SCONJ"]) / self.words
        self.feature_table[47]=len(self.word_dict["CONJ"]) / self.words
        self.feature_table[48]=len(self.word_dict["PUNCT"]) / self.words
        self.feature_table[49]=len(self.word_dict["INTJ"]) / self.words
        self.feature_table[50], x = self.counting_lemma(line1)#20
        self.feature_table[50] /= self.words
        self.feature_table[51] = self.first_person_singular_verbs(line1) / self.words#23
        self.feature_table[52] = self.mis_spell(line1)/self.words#24
        self.feature_table[53], self.feature_table[54] = self.NES(line1)#25 26
        self.feature_table[53] /= self.words
        self.feature_table[54] /= self.words
        self.feature_table[54] = self.neg_analyze(line1) / self.words#28
        self.feature_table[55], self.feature_table[56] = self.content_function(line1)#29 30
        self.feature_table[55] /= self.words
        self.feature_table[56] /= self.words
    
if __name__ == "__main__":
    file_path = '/Users/raychang/Desktop/NTHU Courses/Machine Learning/final_project/Alzheimer-Diagnosis-Speech/linebot/AdamSavage_2008P.txt'
    NLP = NLP_features(file_path)
    NLP.generate_features()
    print(NLP.feature_table)

# Sample output:
# [6.37000000e+02 1.00000000e+00 2.90000000e+01 7.60000000e+01
#  6.40000000e+01 7.60000000e+01 1.29000000e+02 2.90000000e+01
#  1.30000000e+01 1.00000000e+00 8.00000000e+00 9.80000000e+01
#  4.80000000e+01 1.90000000e+01 1.40000000e+01 2.20000000e+01
#  1.00000000e+01 0.00000000e+00 1.30000000e+01 1.00000000e+00
#  2.69000000e+02 3.80000000e+01 1.89000000e+02 1.60000000e+01
#  1.30000000e+01 0.00000000e+00 1.90000000e+01 9.00000000e+00
#  1.90000000e+01 2.89000000e+02 2.92000000e+02 1.56985871e-03
#  4.55259027e-02 1.19309262e-01 1.00470958e-01 1.19309262e-01
#  2.02511774e-01 4.55259027e-02 2.04081633e-02 1.56985871e-03
#  1.25588697e-02 1.53846154e-01 7.53532182e-02 2.98273155e-02
#  2.19780220e-02 3.45368917e-02 1.56985871e-02 0.00000000e+00
#  2.04081633e-02 1.56985871e-03 4.22291994e-01 2.51177394e-02
#  2.04081633e-02 0.00000000e+00 2.98273155e-02 4.53689168e-01
#  4.58398744e-01]

# The output is a bunch of numbers, the attributes of these numbers are shown below.
# ['words_number', 'SPACE', 'ADV', 'VERB', 
#  'ADP', 'DET', 'NOUN', 'ADJ', 
#  'PUNCT', 'INTJ', 'NUM', 'PRON', 
#  'AUX', 'CCONJ', 'PART', 'PROPN', 
#  'SCONJ', 'CONJ', 'Punctuation', 'hestitation_word', 
#  'lemma_number', 'most_frequent', 'noun_chunk', 'person_singular_verbs', 
#  'misspell', 'time_spec', 'spec', 'sentence', 
#  'neg_word', 'content', 'function', 'SPACE_R', 
#  'ADV_R', 'VERB_R', 'ADP_R', 'DET_R', 
#  'NOUN_R', 'ADJ_R', 'PUNCT_R', 'INTJ_R', 
#  'NUM_R', 'PRON_R', 'AUX_R', 'CCONJ_R', 
#  'PART_R', 'PROPN_R', 'SCONJ_R', 'CONJ_R',
#  'Punctuation_R', 'hestitation_word_R', 'lemma_number_R', 'person_singular_verbs_R', 
#  'misspell_R', 'time_spec_R', 'spec_R', 'neg_word_R', 
#  'content_R', 'function_R']