# Machine Learning Model for Alzheimer's Disease Prediction

## Overview
This machine learning model is designed to predict Alzheimer's Disease (AD) using various classifiers. The model is trained on a dataset consisting of AD patients, MCI (Mild Cognitive Impairment) patients, and healthy individuals. The classifiers used include K-Nearest Neighbors, Support Vector Machine, Decision Tree, Random Forest, Neural Network, and a Stacked Model combining these classifiers.

## Requirements
- Python 3.x
- Libraries: pandas, numpy, sklearn, matplotlib

## Installation
Ensure that Python 3 and the required libraries are installed. You can install the libraries using pip:
```
pip install pandas numpy sklearn matplotlib
```

## Usage
### Step 1: Connect to Google Drive
Mount your Google Drive to access the datasets.
```python
from google.colab import drive
drive.mount('/content/drive/')
```

### Step 2: Import Packages
Import all the necessary packages.
```python
import pandas as pd
import numpy as np
...
import matplotlib.pyplot as plt
```

### Step 3: Load and Prepare the Dataset
Load the dataset from your file path and split it into training and test sets.
```python
# Paths to datasets
whole_dataset = ""
...

# Load and prepare the dataset
training_df = pd.read_csv(MCI_AD)
X = training_df.drop(['name', 'AD_diagnose'], axis=1)
y = training_df['AD_diagnose']
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state=20)
```

### Step 4: Feature Selection using Lasso
Perform feature selection using Lasso regression.
```python
lasso_model = Lasso(alpha=0.005)
...
```

### Step 5: Model Training and Evaluation
Train and evaluate different models: KNN, SVM, Decision Tree, Random Forest, Neural Network, and Stacked Model. Each model's performance is evaluated using accuracy, MCC, and F1-score metrics.
```python
# K nearest neighbors
knn = KNeighborsClassifier(10)
...
```

### Step 6: Results Visualization
Visualize the performance of each model.
```python
df.plot(kind = "line")
```

## Data
Ensure that the datasets are correctly placed in your Google Drive. The datasets required are:
- Merged data
- Normalized merged data
- MCI data
- MCI patient data
- Modified result data

## Note
- This model is developed for educational and research purposes.
- The performance of the model can vary based on the quality and size of the dataset used.