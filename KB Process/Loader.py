import logging
import os

import joblib
import numpy as np
import pandas as pd

LOGGER = logging.getLogger('KnowledgeBase')
LOG_FORMAT = '%(levelname) -10s %(name) -45s %(funcName) -35s %(lineno) -5d: %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

class Loader:
    def __init__(self, s3_resource):
        self.bucket_name = 'nsl-kdd-datasets'
        self.s3_resource = s3_resource

    def s3_load(self):
        LOGGER.info(f'Loading data from S3 bucket {self.bucket_name}.')

        LOGGER.info('Loading set of minimal features.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='AdditionalFiles/MinimalFeatures',
            file_name='NSL_features_l1.txt',
            download_path="AWS Downloads/MinimalFeatures/"
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='AdditionalFiles/MinimalFeatures',
            file_name='NSL_features_l2.txt',
            download_path="AWS Downloads/MinimalFeatures/"
        )

        LOGGER.info('Loading set of one hot encoders.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='AdditionalFiles/OneHotEncoders',
            file_name='OneHotEncoder_l1.pkl',
            download_path="AWS Downloads/OneHotEncoders/"
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='AdditionalFiles/OneHotEncoders',
            file_name='OneHotEncoder_l2.pkl',
            download_path="AWS Downloads/OneHotEncoders/"
        )

        LOGGER.info('Loading set of PCA encoders.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='AdditionalFiles/PCAEncoders',
            file_name='layer1_pca_transformer.pkl',
            download_path="AWS Downloads/PCAEncoders/"
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='AdditionalFiles/PCAEncoders',
            file_name='layer2_pca_transformer.pkl',
            download_path="AWS Downloads/PCAEncoders/"
        )

        LOGGER.info('Loading set of scalers.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='AdditionalFiles/Scalers',
            file_name='Scaler_l1.pkl',
            download_path="AWS Downloads/Scalers/"
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='AdditionalFiles/Scalers',
            file_name='Scaler_l2.pkl',
            download_path="AWS Downloads/Scalers/"
        )

        LOGGER.info('Loading models.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='Models/StartingModels',
            file_name='NSL_l1_classifier.pkl',
            download_path="AWS Downloads/Models/StartingModels/"
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='Models/StartingModels',
            file_name='NSL_l2_classifier.pkl',
            download_path="AWS Downloads/Models/StartingModels/"
        )

        LOGGER.info('Loading fully processed train sets.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='ProcessedDatasets/PCAEncoded',
            file_name='KDDTrain+_l1_pca.pkl',
            download_path='AWS Downloads/Datasets/PCAEncoded/'
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='ProcessedDatasets/PCAEncoded',
            file_name='KDDTrain+_l2_pca.pkl',
            download_path='AWS Downloads/Datasets/PCAEncoded/'
        )

        LOGGER.info('Loading target variables for train sets.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='ProcessedDatasets/ScaledEncoded_no_pca',
            file_name='KDDTrain+_l1_targets.npy',
            download_path='AWS Downloads/Datasets/PCAEncoded/'
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='ProcessedDatasets/ScaledEncoded_no_pca',
            file_name='KDDTrain+_l2_targets.npy',
            download_path='AWS Downloads/Datasets/PCAEncoded/'
        )

        LOGGER.info('Loading fully processed validation sets.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='ProcessedDatasets/PCAEncoded',
            file_name='KDDValidate+_l1_pca.pkl',
            download_path='AWS Downloads/Datasets/PCAEncoded/'
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='ProcessedDatasets/PCAEncoded',
            file_name='KDDValidate+_l2_pca.pkl',
            download_path='AWS Downloads/Datasets/PCAEncoded/'
        )

        LOGGER.info('Loading target variables for validation sets.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='ProcessedDatasets/ScaledEncoded_no_pca',
            file_name='KDDValidate+_l1_targets.npy',
            download_path='AWS Downloads/Datasets/PCAEncoded/'
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='ProcessedDatasets/ScaledEncoded_no_pca',
            file_name='KDDValidate+_l2_targets.npy',
            download_path='AWS Downloads/Datasets/PCAEncoded/'
        )

        LOGGER.info('Loading original data sets.')
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='OriginalDatasets',
            file_name='KDDTrain+_with_labels.txt',
            download_path='AWS Downloads/Datasets/OriginalDatasets/'
        )
        self.__aws_download(
            bucket_name=self.bucket_name,
            folder_name='OriginalDatasets',
            file_name='KDDTrain+20_percent_with_labels.txt',
            download_path='AWS Downloads/Datasets/OriginalDatasets/'
        )


    def __aws_download(self, bucket_name: str, folder_name: str, file_name: str, download_path: str):
        local_file_path = os.path.join(download_path, file_name)
        self.s3_resource.download_file(
            bucket_name,
            f'{folder_name}/{file_name}',
            local_file_path,
            Callback=self.__aws_download_callback
        )

    def __aws_download_callback(self, bytes):
        # LOGGER.info(f'Downloaded {bytes} bytes')
        pass

    def load_pca_transformers(self, pca1_file, pca2_file):
        pca1 = joblib.load(f'AWS Downloads/PCAEncoders/{pca1_file}')
        pca2 = joblib.load(f'AWS Downloads/PCAEncoders/{pca2_file}')
        return pca1, pca2

    def load_encoders(self, ohe1_file, ohe2_file):
        ohe1 = joblib.load(f'AWS Downloads/OneHotEncoders/{ohe1_file}')
        ohe2 = joblib.load(f'AWS Downloads/OneHotEncoders/{ohe2_file}')
        return ohe1, ohe2

    def load_scalers(self, scaler1_file, scaler2_file):
        scaler1 = joblib.load(f'AWS Downloads/Scalers/{scaler1_file}')
        scaler2 = joblib.load(f'AWS Downloads/Scalers/{scaler2_file}')
        return scaler1, scaler2

    def load_test_set(self):
        x_test = pd.read_csv('NSL-KDD Encoded Datasets/before_pca/KDDTest+', sep=",", header=0)
        y_test = np.load('NSL-KDD Encoded Datasets/before_pca/y_test.npy', allow_pickle=True)
        return x_test, y_test

    def load_og_dataset(self, file):
        x_df = pd.read_csv(f'AWS Downloads/Datasets/OriginalDatasets/{file}')
        return x_df

    def load_dataset(self, pca_file, targets_file):
        x = joblib.load(f'AWS Downloads/Datasets/PCAEncoded/{pca_file}')
        x_df = pd.DataFrame(x, columns=[f'feature_{i}' for i in range(x.shape[1])])
        y = np.load(f'AWS Downloads/Datasets/PCAEncoded/{targets_file}', allow_pickle=True)
        return x_df, y

    def load_features(self, file_path: str):
        with open(file_path, 'r') as f:
            return f.read().split(',')
