import pickle
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier().fit(X, y)
pickle.dump(model, open("model.pkl", "wb"))
print("model.pkl created")
