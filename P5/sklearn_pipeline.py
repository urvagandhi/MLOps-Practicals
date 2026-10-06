# sklearn_pipeline.py
import pandas as pd
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import numpy as np

# Load dataset directly from sklearn (or online)
iris = load_iris(as_frame=True)
df = iris.frame

# Split features and labels
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create a pipeline: scaling + Naive Bayes
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', GaussianNB())
])

# Train the pipeline
pipeline.fit(X_train, y_train)

# Evaluate the pipeline
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Pipeline Model Accuracy: {accuracy:.2f}")

# Save the pipeline
with open("pipeline.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("Pipeline saved successfully as 'pipeline.pkl'.")

# Load the saved pipeline
with open("pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

# Example input for prediction (same number of features as the training data: 4)
# Let's say this is a new Iris flower data point:
X_new = np.array([[5.1, 3.5, 1.4, 0.2]])

# Make prediction
prediction = pipeline.predict(X_new)

# Print result
print(f"Predicted class: {prediction[0]}")
