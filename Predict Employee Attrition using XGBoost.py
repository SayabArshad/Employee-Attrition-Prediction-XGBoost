#import ibraries
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

#load dataset
df = pd.read_csv('d:/python_ka_chilla/AI Projects/Predict Employee Attrition using XGBoost/Employee-Attrition.csv')

# display first few rows of the dataset
print("Employee Attrition DataSet:\n", df.head())

#basic data preprocessing
#drop irrelevant columns
df = df.drop(['EmployeeNumber', 'Over18', 'StandardHours'], axis=1)

#encode categorical variables
label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le
print("\nEncoded DataSet:\n", df.head())

#define features and labels
X = df.drop('Attrition', axis=1)
y = df['Attrition']  # target variable

#split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#train an XGBoost model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')  
model.fit(X_train, y_train)

#make predictions on the test set
y_pred = model.predict(X_test)

#evaluate the model
print("Model Evaluation Results:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

#Confusion matrix visualization
plt.figure(figsize=(8,6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', xticklabels=['No Attrition', 'Attrition'], yticklabels=['No Attrition', 'Attrition'])
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.show()
#Feature importance visualization
plt.figure(figsize=(10,8))
xgb.plot_importance(model, max_num_features=10)
plt.title('Feature Importance')
plt.show()

# Output:
