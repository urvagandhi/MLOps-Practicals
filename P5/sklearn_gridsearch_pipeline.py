# sklearn_gridsearch_pipeline.py
import pandas as pd
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import numpy as np

# Load dataset directly from sklearn (or online)
iris = load_iris(as_frame=True)
df = iris.frame

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline: scaling + classifier
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', GaussianNB())
])

# Define hyperparameter grid
param_grid = {
    'clf__var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6]  # GaussianNB smoothing parameter
}

# Grid search with cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Best parameters and accuracy
print("Best Parameters:", grid_search.best_params_)
y_pred = grid_search.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Tuned Pipeline Accuracy: {accuracy:.2f}")

# Save the tuned pipeline
with open("pipeline_tuned.pkl", "wb") as f:
    pickle.dump(grid_search.best_estimator_, f)

print("Tuned pipeline saved as 'pipeline_tuned.pkl'")

# Load the saved pipeline
with open("pipeline_tuned.pkl", "rb") as f:
    pipeline_tuned = pickle.load(f)

# Example input for prediction (same number of features as the training data: 4)
# Let's say this is a new Iris flower data point:
X_new = np.array([[5.1, 3.5, 1.4, 0.2]])

# Make prediction
prediction = pipeline_tuned.predict(X_new)

# Print result
print(f"Predicted class: {prediction[0]}")
