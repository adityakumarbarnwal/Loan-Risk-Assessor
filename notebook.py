#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing Libraries
import os
import kagglehub
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
from xgboost import XGBClassifier

import joblib


# In[2]:


# =========================
# Step 2: Download Dataset
# =========================
path = kagglehub.dataset_download("algozee/credit-risk-and-loan-default-analysis-dataset")
print("Path to dataset files:", path)

files = os.listdir(path)
print("Files in dataset folder:")
for f in files:
    print(f)


# In[3]:


# =========================
# Step 4: Load Dataset
# =========================
# Replace this with your actual CSV filename after checking Cell 3
csv_file = [f for f in files if f.endswith(".csv")][0]

file_path = os.path.join(path, csv_file)
df = pd.read_csv(file_path)

print("Dataset loaded successfully!")


# In[4]:


df.head(5)


# In[5]:


df.isnull().sum()


# In[6]:


df.sample(6)


# In[7]:


# =========================
# Step 5: Explore Dataset
# =========================
print("Shape of dataset:", df.shape)
print("\nColumns:\n", df.columns.tolist())
print("\nInfo:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())


# In[8]:


from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer


# In[9]:


# Separate num. and cat. columns
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

print("Numeric Columns:", numeric_cols)
print("Categorical Columns:", categorical_cols)


# In[10]:


target_col = "LoanApproved"

if target_col in numeric_cols:
    numeric_cols.remove(target_col)

if target_col in categorical_cols:
    categorical_cols.remove(target_col)


# In[11]:


# Iterative Imputer for num. columns
iter_imputer = IterativeImputer(random_state=42)

df[numeric_cols] = iter_imputer.fit_transform(df[numeric_cols])


# In[12]:


# Simple Imputer for cat. columns
cat_imputer = SimpleImputer(strategy='most_frequent')

df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])


# In[13]:


print("Missing Values After Imputation:")
print(df.isnull().sum())


# In[14]:


# Encoding Target Variable
print("Unique values in target before encoding:", df[target_col].unique())

if df[target_col].dtype == "object":
    le_target = LabelEncoder()
    df[target_col] = le_target.fit_transform(df[target_col])

print("Unique values in target after encoding:", df[target_col].unique())


# In[15]:


# Target Distribution
plt.figure(figsize=(6,4))
sns.countplot(x=df[target_col])
plt.title("Target Class Distribution")
plt.show()

print(df[target_col].value_counts())


# In[16]:


X = df.drop(columns=[target_col])
y = df[target_col]

print("Feature shape:", X.shape)
print("Target shape:", y.shape)


# In[17]:


print("Shape of raw features (before pipeline):", X.shape)


# In[18]:


X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=42, stratify=y )

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)


# In[19]:


# Feature Scaling
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
])


# In[20]:


pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    ))
])
pipeline.fit(X_train, y_train)


# In[21]:


y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]


# In[22]:


# Evaluation Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))
print("ROC AUC  :", round(roc_auc, 4))


# In[23]:


print(classification_report(y_test, y_pred))


# In[24]:


cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# In[25]:


# Feature Importance
feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': pipeline.named_steps["model"].feature_importances_
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10,6))
sns.barplot(data=importance_df.head(15), x='Importance', y='Feature')
plt.title("Top 15 Important Features")
plt.show()

importance_df.head(15)


# In[26]:


# Save Model & Objects
joblib.dump(pipeline, "pipeline.pkl")
print("Saved files:")
print("- pipeline.pkl")


# In[ ]:




