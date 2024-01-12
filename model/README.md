# Alzheimer's Disease Prediction Model Using MFCC and NLP Features

# Alzheimer's Disease Prediction Models: Comprehensive Guide

## Overview
This comprehensive guide covers three Alzheimer's Disease (AD) prediction models, focusing on machine learning techniques, MFCC data extraction, and a combination of MFCC and NLP features. These models aim to predict AD using various classifiers and data sources, including patient and normal datasets.

## Requirements
- Python 3.x
- Libraries: pandas, numpy, sklearn, matplotlib, csv
- Google Colab for drive mounting and processing

## Installation
1. Install Python 3 and required libraries using pip.
2. Use Google Colab for executing scripts and accessing Google Drive.

## Usage
### Common Steps for All Models
- **Connect to Google Drive**: Use Google Colab to mount your Google Drive for data access.
- **Import Required Packages**: Import Python packages like pandas, numpy, sklearn, os, etc.

### Model-Specific Steps
#### 1. Machine Learning Model for AD Prediction
- **Data Preparation**: Load the dataset from Google Drive and split it into training and test sets.
- **Feature Selection using Lasso**: Perform feature selection using Lasso regression.
- **Model Training and Evaluation**: Train models like KNN, SVM, Decision Tree, etc., and evaluate using metrics like accuracy, MCC, and F1-score.
- **Results Visualization**: Visualize model performance.

#### 2. MFCC Data Extraction Model
- **Data Processing**: Initialize a data processing class for extracting MFCC features.
- **MFCC Feature Extraction**: Process patient datasets to extract MFCC features such as mean, standard deviation, etc.

#### 3. Combined MFCC and NLP Features Model
- **Data Preparation**: Load the dataset from Google Drive and split it into training and test sets.
- **Merge MFCC and Text Data**: Combine MFCC data with NLP textual data and assign AD diagnosis labels.
- **Normalize the Final Dataset**: Merge datasets and normalize by dropping non-normalized features.

### Final Dataset Creation and Saving
- **Create DataFrames and Merge Data**: For all models, create separate DataFrames for different features and merge them.
- **Save Processed Data to CSV**: Export the processed data to CSV files for further analysis.

## Data
- Ensure data files like patient datasets, MFCC feature files, and NLP textual data files are correctly placed in Google Drive.
- Follow specific file paths mentioned in the models' scripts.

## Note
- These models are developed for educational and research purposes.
- The performance of the models can vary based on dataset quality and size.
