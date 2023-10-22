import copy
import pickle

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.svm import SVC
import joblib


def train_models(hp1, hp2):
    """
    :param hp1: n-set of hyperparameters to train layer 1
    :param hp2: n-set of hyperparameters to train layer 2
    :return: trained models for layer 1 and 2 respectively
    """

    # Load completely processed datasets for training
    x_train_l1 = joblib.load('NSL-KDD Encoded Datasets/pca_transformed/pca_train1.pkl')
    x_train_l2 = joblib.load('NSL-KDD Encoded Datasets/pca_transformed/pca_train2.pkl')
    y_train_l1 = np.load('NSL-KDD Encoded Datasets/before_pca/KDDTrain+_l1_targets.npy', allow_pickle=True)
    y_train_l2 = np.load('NSL-KDD Encoded Datasets/before_pca/KDDTrain+_l2_targets.npy', allow_pickle=True)

    # Start with training classifier 1
    classifier1 = RandomForestClassifier(n_estimators=100, random_state=42).fit(x_train_l1, y_train_l1)

    # Now train classifier 2
    classifier2 = SVC(C=0.1, gamma=0.01, kernel='rbf').fit(x_train_l2, y_train_l2)

    # Save models to file
    with open('Models/NSL_l1_classifier.pkl', 'wb') as model_file:
        pickle.dump(classifier1, model_file)
    with open('Models/NSL_l2_classifier.pkl', 'wb') as model_file:
        pickle.dump(classifier2, model_file)

    return classifier1, classifier2


class ModelMaker:

    def __init__(self):
        # load the features obtained with ICFS for both layer 1 and layer 2
        with open('NSL-KDD Files/NSL_features_l1.txt', 'r') as f:
            self.features_l1 = f.read().split(',')

        with open('NSL-KDD Files/NSL_features_l2.txt', 'r') as f:
            self.features_l2 = f.read().split(',')

        # set the categorical features
        self.cat_features = ['protocol_type', 'service', 'flag']

        # load one hot encoders
        self.ohe1 = joblib.load('NSL-KDD Files/one_hot_encoders/ohe1.pkl')
        self.ohe2 = joblib.load('NSL-KDD Files/one_hot_encoders/ohe2.pkl')

        # load pca transformers
        self.pca1 = joblib.load('NSL-KDD Encoded Datasets/pca_transformed/layer1_transformer.pkl')
        self.pca2 = joblib.load('NSL-KDD Encoded Datasets/pca_transformed/layer2_transformer.pkl')

    def pipeline_data_process(self, incoming_data, target_layer):
        """
        This function is used to process the incoming data:
        - The features are selected starting f

        :param target_layer: Indicates if the data is processed to be fed to layer 1 or layer 2
        :param incoming_data: The single or multiple data sample to process
        :return: The processed data received as an input
        """

        data = copy.deepcopy(incoming_data)

        scaler = MinMaxScaler()

        if target_layer == 1:
            to_scale = data[self.features_l1]
            ohe = self.ohe1
            pca = self.pca1
        else:
            to_scale = data[self.features_l2]
            ohe = self.ohe2
            pca = self.pca2

        scaled_data = scaler.fit_transform(to_scale)
        label_enc = ohe.fit_transform(data[self.cat_features])
        label_enc.toarray()
        new_labels = ohe.get_feature_names_out(self.cat_features)
        new_encoded = pd.DataFrame(data=label_enc.toarray(), columns=new_labels)
        processed = pd.concat([scaled_data, new_encoded], axis=1).sort_index(axis=1)

        pca_transformed = pca.transform(processed)

        return pca_transformed
