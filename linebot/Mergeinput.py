import os
import numpy as np
import pandas as pd
import csv
import LearningModel_obj as Model
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import f1_score


def predict(x, y_true, model):
    """make prediction and calculate accuracy"""

    # make prediction
    y_pred = model.predict(x)

    # calculate accuracy
    accuracy = accuracy_score(y_true, y_pred)  # Calculate Accuracy
    mcc = matthews_corrcoef(y_true, y_pred)  # Calculate MCC
    f1 = f1_score(y_true, y_pred, average='weighted')  # Calculate F1-score

    print('- Accuracy: %s' % accuracy)
    print('- MCC: %s' % mcc)
    print('- F1 score: %s' % f1)


#MFCC data extraction
class data_process:

    def __init__(self):
        self.labels = []
        self.mean_features = []
        self.std_features = []
        self.var_features = []
        self.min_features = []
        self.max_features = []

    def cal_mfcc_features(self, df):
        self.mean_features.append(df.mean(axis=0))  # mean value of each frame
        self.std_features.append(
            df.std(axis=0))  # standard deviation of each frame
        self.var_features.append(df.var(axis=0))  # variance of each frame
        self.min_features.append(df.min(axis=0))  # minimum of each frame
        self.max_features.append(df.max(axis=0))  # maximum of each frame


class DataMerge():
    
    """Input file path, this class will read in files and output a merged one """
    
    def  __init__(self, NLP_input, mfcc_input, merged_data):
        self.nlp_path = NLP_input
        self.mfcc_path = mfcc_input
        self.final_path = merged_data

    def merge(self):

        dp = data_process()
        
        mean_names = ["mean_0", "mean_1", "mean_2", "mean_3", "mean_4", "mean_5", "mean_6", "mean_7", "mean_8", "mean_9", "mean_10", "mean_11"]
        std_names = ["std_0", "std_1", "std_2", "std_3", "std_4", "std_5", "std_6", "std_7", "std_8", "std_9", "std_10", "std_11"]
        var_names = ["var_0", "var_1", "var_2", "var_3", "var_4", "var_5", "var_6", "var_7", "var_8", "var_9", "var_10", "var_11"]
        min_names = ["min_0", "min_1", "min_2", "min_3", "min_4", "min_5", "min_6", "min_7", "min_8", "min_9", "min_10", "min_11"]
        max_names = ["max_0", "max_1", "max_2", "max_3", "max_4", "max_5", "max_6", "max_7", "max_8", "max_9", "max_10", "max_11"]

        #read in mfcc file
        aud_df = pd.read_csv(self.mfcc_path, header=None)

        audio_names = "Ub1e82ffd0b71b067b7196330dcff2aee"
        
        dp.cal_mfcc_features(aud_df)

        mean_df = pd.DataFrame(dp.mean_features)
        mean_df.columns = mean_names
        mean_df["name"] = audio_names
        mean_df = mean_df.reindex([
            "name", "mean_0", "mean_1", "mean_2", "mean_3", "mean_4", "mean_5",
            "mean_6", "mean_7", "mean_8", "mean_9", "mean_10", "mean_11"
        ], axis=1)

        std_df = pd.DataFrame(dp.std_features)
        std_df.columns = std_names
        std_df["name"] = audio_names

        var_df = pd.DataFrame(dp.var_features)
        var_df.columns = var_names
        var_df["name"] = audio_names

        min_df = pd.DataFrame(dp.min_features)
        min_df.columns = min_names
        min_df["name"] = audio_names

        max_df = pd.DataFrame(dp.max_features)
        max_df.columns = max_names
        max_df["name"] = audio_names

        mfcc_df = pd.merge(mean_df, std_df, how="right", on="name")
        mfcc_df = pd.merge(mfcc_df, var_df, how="right", on="name")
        mfcc_df = pd.merge(mfcc_df, min_df, how="right", on="name")
        mfcc_df = pd.merge(mfcc_df, max_df, how="right", on="name")
        header_list = ['words_number', 'SPACE', 'ADV', 'VERB', 
         'ADP', 'DET', 'NOUN', 'ADJ', 
         'PUNCT', 'INTJ', 'NUM', 'PRON', 
         'AUX', 'CCONJ', 'PART', 'PROPN', 
         'SCONJ', 'CONJ', 'Punctuation', 'hestitation_word', 
         'lemma_number', 'most_frequent', 'noun_chunk', 'person_singular_verbs', 
         'misspell', 'time_spec', 'spec', 'sentence', 
         'neg_word', 'content', 'function', 'SPACE_R', 
         'ADV_R', 'VERB_R', 'ADP_R', 'DET_R', 
         'NOUN_R', 'ADJ_R', 'PUNCT_R', 'INTJ_R', 
         'NUM_R', 'PRON_R', 'AUX_R', 'CCONJ_R', 
         'PART_R', 'PROPN_R', 'SCONJ_R', 'CONJ_R',
         'Punctuation_R', 'hestitation_word_R', 'lemma_number_R', 'person_singular_verbs_R', 
         'misspell_R', 'time_spec_R', 'spec_R', 'neg_word_R', 'content_R']
#         print(len(header_list))
        txt_df = pd.read_csv(self.nlp_path, header=None)
        txt_df.columns = header_list
        txt_df["name"] = audio_names
        drop_cols = ['SPACE', 'ADV', 'VERB', 'ADP', 'DET', 'NOUN', 'ADJ', 'PUNCT', 
                     'INTJ', 'NUM', 'PRON', 'AUX', 'CCONJ', 'PART', 'PROPN', 'SCONJ',
                     'CONJ', 'Punctuation', 'hestitation_word', 'lemma_number', 
                     'most_frequent', 'noun_chunk', 'person_singular_verbs', 'misspell',
                     'time_spec', 'spec', 'sentence', 'neg_word', 'content', 'function']
        print(len(drop_cols))
        txt_df = txt_df.drop(drop_cols, axis = 1)
        #merge txt and mfcc
        merged_input_df = pd.merge(mfcc_df, txt_df, how="right", on="name")
        merged_input_df.drop(["name"], axis = 1, inplace = True)
        #write csv into final path
        merged_input_df.to_csv(self.final_path, index=False)

        merged_data = np.array(pd.read_csv("/tmp/merge.csv"))
        print(merged_data.shape)
        
if __name__ == "__main__":

    data_integration = DataMerge("nlp.csv", "mfcc.csv", "merge.csv")
    data_integration.merge()


